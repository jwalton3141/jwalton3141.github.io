---
layout: post
title: Scaling R with AWS Lambda
slides: /assets/talks/r_with_aws_lambda.pdf
---

In this talk I gave an overview of a recent client project in which AWS
Lambda was used to provide a scalable R-backend for a public-facing web
application. This backend performed a number of different operations,
including; evaluating a Bayesian Network model; rendering a parameterised PDF
report via [R Markdown](https://rmarkdown.rstudio.com/), and creating data
visualisations with [{ggplot2}](https://ggplot2.tidyverse.org/).

The frontend and backend code for this application is available publicly on
GitHub [here](https://github.com/nationalarchives/DiAGRAM).
Similarly, the infrastructure as code to host the front and backend is
available [here](https://github.com/nationalarchives/DiAGRAM-terraform/).

I gave this talk at the [North East Data Science meetup in September 2022](https://jumpingrivers.github.io/neds-meetup-2022/2022-09-15/).
