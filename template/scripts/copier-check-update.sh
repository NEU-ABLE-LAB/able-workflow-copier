#!/bin/bash

# Check for available copier updates for each answer file in .copier-answers/
for answer_file in .copier-answers/*.yml; do
    [ -f "${answer_file}" ] || continue
    copier check-update --answer-file "${answer_file}"
done
