# Introduction
Chaos-engineering for Kubernetes using [Robusta](https://github.com/robusta-dev/robusta)

1. Generate OOMs
2. Generate high cpu 
3. Make nodes unresponsive by creating kubelet issues

More to come soon!

# Why another chaos engineering tool
Because we love Python.

We want chaos engineering to be simpler.

We want to make the chaos scenarios easily understandable by everyone who knows a little Python.

We want to make it easier to add your own chaos scenarios specific to your company.

Robusta lets us do all of that with one simple Python function per chaos scenario.

# Is it really that simple?
Yes! Look at the code for the [kill_node](https://github.com/robusta-dev/robusta-chaos/blob/master/robusta_chaos/node_killer.py) action.

This is invoked using:

```bash
robusta playbooks trigger kill_node name=<node-name>
```

All the wiring and annoying parts are handled by Robusta. The `kill_node` action contains logic but no boilerplate wiring.

[See the Robusta docs on manual triggers to understand how this works.to understand how this works.](https://docs.robusta.dev/master/getting-started/manual-triggers.html)
