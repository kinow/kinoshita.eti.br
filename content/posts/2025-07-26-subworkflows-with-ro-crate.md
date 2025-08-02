---
title: "Migrating the Jena editor from CodeMirror 5 to 6"
date: 2025-06-25T09:38:52+03:00
categories:
  - blog
tags:
  - opensource
  - javascript
  - programming
images:
  - '/assets/posts/2025-06-28-migrating-the-jena-editor-from-codemirror-5-to-6/01.png'
---

https://github.com/common-workflow-language/user_guide/blob/main/src/_includes/cwl/workflows/nestedworkflows.cwl
https://github.com/common-workflow-language/user_guide/blob/3bfa62397cece91175f3652e2df7d8b43beb0c15/src/_includes/cwl/workflows/nestedworkflows.cwl

https://github.com/Language-Research-Technology/ro-crate-html-js

https://gitlab.com/dtgeo/metadata/cwl-ro-crate


pip install git+https://github.com/common-workflow-language/cwltool.git@dd5ece01dd0993f0831e25b1b84394fd9f672c1b
pip install git+https://github.com/ResearchObject/runcrate.git@e0da7976dfc711376d84d6dcb78e48a98c306814
cwltool --no-match-user --provenance nestedworkflows --orcid https://orcid.org/0000-0001-8250-4074 --full-name "Bruno P. Kinoshita" --enable-user-provenance --enable-host-provenance nestedworkflows.cwl
runcrate convert --output nestedworkflows-rocrate nestedworkflows


Describo
© Marco La Rosa, 2023 - present. v0.49.2


