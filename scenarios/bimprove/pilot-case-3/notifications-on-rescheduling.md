# Notifications on Rescheduling 

## Summary

The construction of a larger building requires complex planning. 
An initial planning can be carried out on the basis of a BIM representation 
of the building (BIM 4D or separate scheduling tool). 
A wide variety of events, such as weather-related work stoppages, 
delivery delays, errors in construction work, etc., however, require 
ongoing rescheduling that is adapted to current needs. 
Planning is made more difficult by unforeseen events, especially for 
the trades that follow the buildings' shell construction.

## Models

<model name="plan/main">

This is the main model of the site plan covering the whole site.
It is updated on demand, as the plan changes.
The schedule and cost items are part of this plan.

The plan is versioned and every version can be retrieved.

</model>

## Definitions

<def name="DownstreamTasks">

Downstream tasks is a function that selects all the tasks dependent on 
one or more ancestor tasks which need to be finished before the downstream 
task can be executed.

```bim
TaskIsDownstream(t: IfcTask, maybeAncestor: IfcTask) =
    ??? (need BIM expertise here)

DownstreamTasks(tasks: IfcTask[]) =
    SELECT
        dt
    FROM
        t in tasks
        dt is IfcTask modeled in plan/main
    WHERE
        TaskIsDownstream(t, dt)
```

</def>

<def name="ListenersOnTask">

Listeners on task are all the groups of both people and services that need to 
be notified when a task is re-scheduled.

```bim
ListenersOnTask(t: IfcTask) =
    SELECT
        g
    FROM
        g is IfcGroup modeled in plan/main
    WHERE
        EXISTS
            r
        FROM
            r is IfcRelationship in plan/main
        WHERE
            g should be notified 
            ??? (need BIM expertise -- how to model these relations properly?)
```

??? Is it groups or individual services/people? ???

??? Should services be modeled as well or only people as IfcActor? ???

??? Should services be IfcActor as well? ???

??? Or should we only lay down the notification channel (e.g., in form of 
URL) so that we do not care who is notified (tradeoff: no analytics / reasoning
on notifiers possible any more)? ??? 

</def>

## Scenario

### As-planned

All the tasks and cost items should be tracked in the model 
<modelref name="plan/main" />.

### Schedule

On every change to the task, all the downstream tasks need to be rescheduled.
The groups of actors affected by the change should be notified.

??? *should be notified* -- based on their default notification channel? Do we 
support multiple notifications channels? ???

??? are changes performed task-per-task or multiple tasks change at once in a
transaction? I assume multiple tasks per transaction -- rescheduling one task
will affect other tasks and they will be (automatically or manually) changed 
in the plan? ???

```bim
NOTIFY
    g with Message(tt)

FROM
    g is IfcGroup modeled in plan/main
    tt are IfcTask's modeled in plan/main
    
    dtt = Set(DownstreamTasks(tt) + tt)
    
    listeners =
        SELECT
            ListenersOnTask(t)
        FROM
            t in tt

WHERE
    g in listeners

TRIGGERED BY
    tt rescheduled (??? need BIM expertise -- how do you model rescheduling?)
```

??? what about deletion of tasks? ???

??? should the downstream tasks be automatically postponed and how? ???

??? Is there a rescheduling type in BIM? E.g. to give a reason for the 
rescheduling such as "weather"? Do we need to notify the listeners with the
reason at all? Would that be a nightmare to maintain if security comes into
play (e.g., notify some listeners only that the task changed and yet other
listeners with the task + the cause based on authorization)? ???

??? Who is authorized to make the changes to schedule? ???

??? Should the changes to schedule be reviewed? By whom? 
How do we model the review process? (probably as BCF?) ???

??? Is this what this scenario is meant for -- mere notification on 
rescheduling? Or was it aimed to automatically discover when something needs
to be rescheduled? These are huge question marks! The former case is much 
simpler than the latter! ???
