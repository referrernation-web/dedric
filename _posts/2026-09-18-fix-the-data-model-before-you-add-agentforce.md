---
layout: post
title: "Fix the data model before you add Agentforce"
description: "Every AI use case I have evaluated on Salesforce came down to one question first: can we trust the records underneath it?"
date: 2026-09-18
tags: [Agentforce, Data governance, Salesforce]
cover:
hidden: true
---

> DRAFT FOR DEDRIC'S REVIEW. This page is not listed on the blog and search engines are told not to index it. Edit it in the admin, then switch "Hidden" off to publish.

I have one operating rule for AI on Salesforce: fix the data model and the automation before layering Agentforce or Einstein on top. It sounds obvious. It is also the step most roadmaps skip, because the demo works on clean sample data and production does not look like sample data.

## The use case is never the hard part

At Centene I own the AI enablement roadmap for the specialty pharmacy and managed care lines. Prior authorization, benefits investigation and referral-to-therapy are the obvious targets. Picking them took an afternoon.

The harder question was whether the records behind each workflow could be trusted. Three systems, ScriptMed, the Centene prescriber file and Symphony Health, each described the same provider differently. An agent that reads three versions of one provider does not save anyone time. It produces a confident answer about the wrong record.

## Gate each use case on data readiness

So each use case gets gated on data readiness before automation and AI:

- **One identity per provider.** We standardized the provider and member data models and keyed external IDs on the National Provider Identifier (NPI).
- **Duplicates removed, and rules that keep them out.** Deduplication is not a one-time cleanup.
- **Controls Compliance can review.** In a HIPAA-regulated business, "the model decided" is not an answer.

Some workflows cleared the gate. Others were held back until their data was fixed. Holding a use case back is a product decision, not a failure.

## I learned this before AI

The same pattern showed up at Cloudflare, years before anyone said "agent". Opportunity, order, billing and revenue recognition lived in Salesforce and NetSuite, and the two never agreed. We settled external IDs and reconciliation rules first, then built the dashboards. Time-to-insight dropped 40% and 12+ teams adopted the reporting, because people could finally trust the number on the screen.

AI raises the stakes on the same problem. A dashboard on bad data gets questioned. An agent on bad data gets believed.

## What to do on Monday

1. List the AI use cases your leadership is excited about.
2. For each one, name the objects and fields it reads, and who owns them.
3. Ask whether you would let a new hire act on those records without checking. If not, the agent should not either.
4. Put the data fix on the roadmap ahead of the agent, with its own success metric.

The teams that do this ship AI later than the teams that do not. They also keep it in production.
