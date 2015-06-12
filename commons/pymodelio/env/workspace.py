# -*- coding: utf-8 -*-

#
#
#
# [code]
# MyWorkSpace/
#    macros/              # you can safely use github for this directoy, regular stuff
#       .catalog          # an XML file that explain how python files below become macros
#       myMacro1.py       # your macros
#       myMacro1.py
#       ...
#    MyProject1/
#      project.conf       # don't touch. XML. Refs to fragments, modules and props.
#      data/
#         .config/
#             styles/      # Styles for the projet. Safe IMHO to play with.
#                 default.style    # The root style
#                 ...      # Don't break the style hierarchy (basestyle=...)
#         fragments/
#             PredefinedTypes X.Y.Z/   # always there.
#                 ...      # you can use this fragment to understand better the internals
#                          # Compare this with what the interface shows
#             ModelerModule/     # idem
#             MyProject1/  #
#                 content
#
#             ...         # Some other fragments. See Work Models, Libraries in the configuration interface
#         modules             # This directory could be big. Can be probably rebuild
#             ModelerModule/  # obviously if you store these files
#             OtherModule/
#                  OtherModules.jmdac    #
#      .runtime
#
#    MyProject2
#    ...
# [/code]
