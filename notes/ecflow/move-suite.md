# Move a suite between two ecFlow 5.8.x servers

*Reference: [Moving suites between ecFlow servers](https://confluence.ecmwf.int/display/ECFLOW/Moving+suites+between+ecFlow+servers)*

The user marks a node to be moved in the `ecflow_ui`, and then tells the UI to move the node to somewhere:

1. [`VNodeMover::moveMarkedNode`](https://github.com/ecmwf/ecflow/blob/08fcc175fcc3cea5e480afc858f209a26ead724b/Viewer/ecflowUI/src/VNodeMover.cpp#L113-L128)
   performs a series of verifications (same host, configuration exists, etc.)
   and if the user confirms the action in the UI, then it instructs the server
   to schedule a task `VTask::PlugTask` to be run;
2. [`ServerComThread::run`](https://github.com/ecmwf/ecflow/blob/5ba3d12d364bee7a29783b5c1d254fd8fdc22fe2/Viewer/ecflowUI/src/ServerComThread.cpp#L215-L220)
   will pick up this task in its next execution, and then will ask the
   `ClientInvoker` to “plug” the source to the target;
3. [`ClientInvoker::plug`](https://github.com/ecmwf/ecflow/blob/38d7e1c25f07a62e785256c0ffabb5106ee4f807/Client/src/ClientInvoker.cpp#L1115-L1119)
   will invoke a new `PlugCmd` with source and target destination paths as arguments.
4. [`PlugCmd::doHandleRequest`](https://github.com/ecmwf/ecflow/blob/08fcc175fcc3cea5e480afc858f209a26ead724b/Base/src/cts/PlugCmd.cpp#L155-L197) performs similar verifications as in `VNodeMover::moveMarkedNode`,
   then after it has confirmed everything looks OK, and the destination is another `ecflow_server`,
   it will authenticate to the other server (same user ans password of logged-in
   user) and then the `ecflow_server` appears to call same API used in `ecflow_client`,
   to send a client request to the other server to execute `MoveCmd`;
5. [`MoveCmd::doHandleRequest`](https://github.com/ecmwf/ecflow/blob/08fcc175fcc3cea5e480afc858f209a26ead724b/Base/src/cts/PlugCmd.cpp#L384-L394)
   also runs some verification checks to make sure it can safely move the suite (node).
   It handles cases like when you move a node that conflicts with an existing node
   (e.g. a suite matches the name of a task, I think; then it will make the task a
   child of the suite?). But if all the checks pass, it creates an object with the
   suite source, and then add it to the list of definitions in the server (same as
   if you create a suite with `ecflow_client` or the Python API).
