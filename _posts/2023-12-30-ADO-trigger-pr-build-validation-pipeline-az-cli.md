---
layout: post
title: Trigger Azure DevOps PR build validation pipelines with az cli
comments: true
---

[Branch policies in Azure DevOps (ADO)](https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies) can be used to protect important branches. 
With branch policies, it's possible to enforce, for example, that all pull
requests into your `main` branch are given a minimum number of approvals before
being allowed to complete.

One could also enforce that all such pull requests successfully run a
particular [ADO pipeline](https://learn.microsoft.com/en-us/azure/devops/pipelines/get-started/what-is-azure-pipelines).
This is a great way to ensure that proposed changes pass particular unit tests,
don't break existing functionality, and conform to agreed coding conventions
for your project.

<p align="center">
<img src="/assets/posts/ado_trigger_build_pipeline/add_build_policy.png" alt="Adding a build policy to a branch.">
</p>

Branch policies can then be viewed as a useful tool in helping maintain and
enforce quality control on code that is allowed into production, or other
important environments and branches.

## Azure DevOps with the Azure CLI

The [Azure Command Line Interface](https://learn.microsoft.com/en-us/cli/azure/what-is-azure-cli)
(`az cli`) is an invaluable tool which can be used to interact with Azure
resources in a programmatic manner.

Using the [Azure CLI DevOps extension](https://learn.microsoft.com/en-us/cli/azure/service-page/devops?view=azure-cli-latest),
a developer can programmatically interact with Azure DevOps. This allows a
developer to automate their repetitive Azure DevOps tasks and typical
workflows.

A developer can, for example, use the `az pipelines` command group to trigger
ADO pipeline runs against their code, branch or PR. However, if a developer is
working on a PR into a branch which requires a successful pipeline run to
complete, in the form of a branch policy, their `az pipelines` triggered run
won't count towards this requirement.

Instead, to trigger a pipeline with the Azure CLI so that it counts towards a
PR's branch policies, as if you had pressed the queue button from your PR, it's
necessary to use the `az repos pr policy` command.

<p align="center">
<img src="/assets/posts/ado_trigger_build_pipeline/queue_pipeline.png" alt="Queuing a build policy pipeline from a PR.">
</p>


## Triggering build validation pipelines with the Azure CLI

To trigger a pipeline run against a PR that will count towards the target
branch's validation policies, we will need to work out our build validation
evaluation ID. Note that this value changes on a _per_ PR basis.

However, to determine our build validation evaluation ID, we first need our PR
number! We can get our PR number a few different ways; from ADO's UI (it's the
number after the `!`); from our PR's URL (it's the number after
`/pullrequest/`), or if we created our PR with the Azure CLI in the first
place:

```sh
az repos pr create \
  --repository $(basename -s .git `git config --get remote.origin.url`) \
  --source-branch $(git branch --show-current) \
  --target-branch main \
  --query "pullRequestId"
```

Once we have our PR number, we can determine the build validation evaluation ID
with:
```sh
az repos pr policy list \
    --id <YOUR-PR-NUMBER-HERE> \
    --query "[?configuration.type.displayName=='Build'].evaluationId"
```

To extract the information we need (the build evaluation ID) we pass a
[JMESPath query](https://jmespath.org/) to the `--query` argument. Without this
we'd be returned a large and verbose JSON response, detailing the policies that
apply to our PR, which user created the policies, and when, and details about
that user.

The extracted evaluation ID will be a long alpha-numeric string, delimited with
hyphens. It'll look something like: `"d2hr35yd-9fe0-y4t5-hb35-5een2cr04b2"`.

We then need to pass this value, unquoted, to `az repos pr policy queue` as:
```sh
az repos pr policy queue \
    --evaluation-id <BUILD-EVAL-ID-HERE> \
    --id <YOUR-PR-NUMBER-HERE>
```

We can combine this two-step process into a single script by performing a
little string manipulation between the steps:
```sh
# Your PR number here
pr_id=123

build_pipeline_eval_id=$(
  az repos pr policy list \
      --id $pr_id \
      --query "[?configuration.type.displayName=='Build'].evaluationId | [0]" \
      --out tsv
)
az repos pr policy queue --evaluation-id $build_pipeline_eval_id --id $pr_id
```

The usage of `--out tsv` removes the surrounding quotes from the build
evaluation ID. This is required as the `az repos pr policy queue` expects this
argument without quotes. Rather than `--out tsv`, we could have piped the
output into a `sed` command such as `sed s/"//g`, or performed the JSON
querying with `jq -r` rather then `--query`. However, `--out tsv` is chosen
here as it does not require any other programs to be installed.

This will now run our required build pipeline, against our PR, as if we had
clicked the "Queue" button from the ADO UI, as desired!

Having the ability to trigger such a pipeline run from the Azure CLI opens up
lots of other opportunities for automating our tedious and repetitive Azure
DevOps tasks.
