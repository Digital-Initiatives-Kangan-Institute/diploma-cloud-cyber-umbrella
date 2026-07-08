"""Shared, reusable helpers for the build scripts.

Modules here hold ONLY generic, reusable building blocks (python-docx / python-pptx
primitives, brand styling). They are imported BY the cluster and scenario build
scripts — they must never import an end-product builder.

End products (the cluster/AT/scenario builders) are leaves: they consume helpers,
and nothing consumes them. If two builders need the same code, it belongs here.
"""
