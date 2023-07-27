---
layout: post
title: In Defence of the Humble Pie Chart
comments: true
---

If you're active in any Data Science communities---whether on Twitter, Reddit,
LinkedIn, Discord, or wherever else---you've probably already encountered a
member of the pie chart hate-brigade. In fact, in reading this post, there is a
good chance that you're _already_ a member of this group, rallying to heap
further criticism on your least favourite graphic!

Yes, data science communities are now _littered_ with posts and comments
maligning the much-scorned pie chart. One really doesn't have to spend too much
time browsing these communities to see the pie chart receiving a good
lambasting. Users criticise pie charts with many, often tiny, incomparable
segments; the pie chart's inability to communicate precise numbers, and their
general inferiority to bar charts.

<!--
fig, ax = plt.subplots(1, 2, figsize=(10, 5))

x = [35, 25, 15, 10, 5, 4, 3, 1]
labels = ["Dogs", "Cats", "Rabbits", "Guniea Pigs", "Hamsters", "Parrots", "Tortoises", "Snakes"]
ax[0].pie(
    x,
    labels=labels,
    autopct=lambda p: '{:.2f}%'.format(p),
)
ax[0].set_title("Most popular UK pets")

x = [27, 25, 26, 23]
labels = ["Tea", "Coffee", "Pop", "Water"]
ax[1].pie(
    x,
    labels=labels,
    shadow=True,
    explode=([0] * (len(x) - 1) + [0.1])
)
ax[1].set_title("Favourite soft drinks")

fig.tight_layout()
fig.savefig("questionable_pies.png")
-->

![Questionable Pie Charts](/assets/posts/pies/questionable_pies.png)

And truthfully, _these criticisms have weight_. It is undoubtedly true that pie
charts are frequently used in situations where another graph would have been
more appropriate. Pie charts with many segments generally can be difficult to
read, and it really is hard to make comparison between several similarly
sized pie chart segments.

However, the pie chart's misuse does not mean that it is an _inherently bad_
graphic. Perhaps there's no such as thing as an inherently bad graph, only bad
communicators.

Additionally, what was once a "hot-take" in data visualisation has now become
so often mindlessly parroted, that the debate itself has lost meaning and any
semblance of nuance, deteriorating into a "pie chart bad; bar chart good"
groupthink.

So, when might a pie chart be an appropriate choice of graphic? To think about
this, we're going to consider:

1. The _type_ of data we're trying to visualise;
2. The _story_ we're trying to tell;
3. The _context_ in which we'll be displaying our graphic.

Considering points 1. and 2., I might conclude that an appropriate time to use a
pie chart would be in situations when there is only a small number of groups to
visualise (2--3 groups, or perhaps 4, at a push), and where accurate comparisons
between similarly-sized groups is _not_ required.

Context (point 3.) is a very important consideration for what is an appropriate
choice of graph too. Is your graph to be inserted into a technical report or
paper, where motivated individuals will have time to inspect your graph at their
own leisure, inspect your axes, draw their own conclusions, and so on? Or is
your visualisation to be used in a PowerPoint presentation to a marketing team,
where your slide will only be on-screen for a short period of time, and you want
to keep your messaging clear and simple?

<!--
plt.style.use("ggplot")

fig, ax = plt.subplots(figsize=(10, 5))

x = [72, 18]
labels = ["No", "Yes"]
ax.pie(
    x,
    labels=labels,
    labeldistance=0.5,
    startangle=90,
)
ax.set_title("Are you aware of brand X?")

fig.tight_layout()
fig.savefig("better_pie.png")
-->

![Better Pie Chart](/assets/posts/pies/better_pie.png)

Consider the above plot. This pie chart may be a perfectly good choice of
graphic to display in a powerpoint presentation to a marketing team, where the
message we're trying to communicate is "We have low brand-recognition". Note
that the exact numbers might not be particular important in this context: we
might not _really care_ if 16% vs 19% of people were aware of our brand, the
point is that the _majority of people_ surveyed weren't brand-aware. And sure,
we _could_ have added the exact numbers to this plot, but if we don't _need_ the
numbers to communicate our message, we're just adding unnecessary and potentially
distracting noise to our presentation.

But that's enough about pie charts. My argument in this post really isn't
supposed to be "pie charts are good", nor is it _really_ about pie charts at
all.  What I'm trying to argue is that _all_ graph types have their pros and
cons, as well as situations when they are and aren't appropriate.  My argument is
that as data communicators, we should always strive to choose the graphic which
best communicates our message, in the given context, _regardless_ of what graph
that might be. My argument is that we should always think critically about how
we might best visualise our data, and that graphical-dogma hardly seems the best
way to go about this.