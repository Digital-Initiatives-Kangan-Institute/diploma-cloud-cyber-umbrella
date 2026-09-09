# Test plan — factory

Every case the factory commits to covering, and the test function that covers it. Built test-first: cases
are agreed here, tests are written against them, then the code is written to pass. The **Test function**
column is the auditable trail — an empty cell means the case is agreed but not yet covered.

`factory/` is one unit of development, so this is its single plan. See
[test-first-process.md](../../docs/test-first-process.md) for the process and
[factory/README.md](../README.md) for the structure.

## Prefix legend

Case IDs are prefixed by the surface they cover, and never renumbered (retire an ID rather than reuse
it). Helper prefixes name the module; step prefixes are the process letter plus the step number, so a
case ID says where in the factory the behaviour lives.

| Prefix | Surface it covers |
|---|---|
| HFC | `common/helpers/format_contract.py` — locating a format doc, parsing its `## Skeleton` contract |
| HNUM | `common/helpers/numeric.py` — number coercion and display used in validator reporting |
| HMDT | `common/helpers/md_table.py` — reading markdown tables out of a document |
| HUS | `common/helpers/uoc_sections.py` — which UoC sections a Topic teaches, in institutional vocabulary |
| HDT | `common/helpers/docx_template.py` — filling an institutional .docx template without disturbing its formatting |
| HLLN | `common/helpers/lln_requirements.py` — deriving a cluster's LLN requirements from its units' Foundation Skills |
| CDP | `process_03_delivery/step_06_cluster_delivery_plan/` — `validate_cluster_delivery_plan.py` |
| CDG | `process_03_delivery/step_06_cluster_delivery_plan/` — `build_cluster_delivery_plan.py` (the docx generator) |

A prefix names the **surface** — a module or an artefact — not its position in the factory. Step numbers
are deliberately absent: steps are retired rather than renumbered, so a positional prefix would go stale
the moment a step moved, and the linter's ID grammar (`[A-Z]{1,5}-\d{1,3}`) admits letters only. Add a
row here when a new surface gains its first case.

## Fixtures

The fake objects the suite needs, named and purposed.

| Fixture | Purpose |
|---|---|
| `format_doc` | writes a minimal format document containing a `## Skeleton` fenced block, so contract parsing is tested against a real file rather than an inline string |
| `doc_tree` | builds a temporary directory tree (a step folder, a nested `scripts/` dir, an umbrella-style `docs/` dir) so document lookup can be tested from several starting points |
| `cluster` | builds a temporary cluster: `cluster-specification.md`, `delivery/topic_NN/` dirs, `assessments/AT<n>/` dirs, and a `delivery/delivery-plan.md` — the real on-disk shape the validator reads |
| `plan_text` | a valid baseline outline (title, INSTANCE banner, prerequisites, a complete session grid) that a test mutates to produce exactly one defect |
| `run_validator` | invokes the validator against a plan and returns `(exit_code, stdout)`, so each case asserts the verdict and the message a human would act on |

## Cases

### HFC — `format_contract.py`

`find_format_doc(name, explicit=None, start=None)` — locate the format document a validator is driven by.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HFC-01 | an explicit path that exists is returned unchanged | `test_explicit_path_that_exists_is_returned` |
| HFC-02 | an explicit path that does not exist returns None | `test_explicit_path_that_is_missing_returns_none` |
| HFC-03 | the document is found beside the starting directory | `test_found_beside_the_starting_directory` |
| HFC-04 | the document is found in a `docs/` directory while walking up from the start | `test_found_in_a_docs_dir_walking_up` |
| HFC-05 | a number-prefixed variant (`_02_<name>`) is found beside the starting directory — the factory step-folder convention | `test_number_prefixed_variant_is_found` |
| HFC-06 | None is returned when the document is nowhere on the search path | `test_returns_none_when_nowhere_on_the_path` |
| HFC-07 | the nearest match wins when the document exists at more than one level | `test_nearest_match_wins` |

`parse_contract(format_text)` — read the machine-readable contract out of the `## Skeleton` block.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HFC-08 | `##` headings inside the Skeleton block are returned, de-duplicated, in document order | `test_headings_are_returned_in_order_deduplicated` |
| HFC-09 | `- Label:` field names inside the Skeleton block are returned | `test_labelled_field_names_are_returned` |
| HFC-10 | the column names of the first table header row in the block are returned | `test_grid_columns_come_from_the_first_header_row` |
| HFC-11 | the table separator row is not mistaken for a header row | `test_separator_row_is_not_read_as_a_header` |
| HFC-12 | three empty lists are returned when there is no `## Skeleton` block | `test_no_skeleton_block_returns_three_empty_lists` |
| HFC-13 | headings and fields outside the Skeleton block are ignored | `test_content_outside_the_skeleton_is_ignored` |

`parse_labelled_fields(text)` — read `- Label: value` lines from a document body.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HFC-14 | `- Label: value` lines are read into a mapping | `test_labelled_lines_are_read_into_a_mapping` |
| HFC-15 | lines that are markdown table rows are ignored | `test_table_rows_are_ignored` |
| HFC-16 | a repeated label keeps the last value | `test_repeated_label_keeps_the_last_value` |
| HFC-17 | a line with no colon is ignored | `test_line_without_a_colon_is_ignored` |
| HFC-18 | an indented line after a labelled field continues that field's value | `test_indented_line_continues_the_field` |
| HFC-19 | continuation ends at the next unindented line | `test_continuation_ends_at_the_next_unindented_line` |
| HFC-20 | a continued value keeps its line breaks, so a document can render it as written | `test_continued_value_keeps_its_line_breaks` |

### HNUM — `numeric.py`

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HNUM-01 | an integer is parsed out of a string | `test_integer_is_parsed_from_a_string` |
| HNUM-02 | a decimal is parsed out of a string | `test_decimal_is_parsed_from_a_string` |
| HNUM-03 | a unicode minus (`−`) is read as a negative sign | `test_unicode_minus_is_read_as_negative` |
| HNUM-04 | None is returned when the string contains no number | `test_string_without_a_number_returns_none` |
| HNUM-05 | None is returned for a None input | `test_none_input_returns_none` |
| HNUM-06 | an integral value is displayed without a decimal point | `test_integral_value_displays_without_a_decimal_point` |
| HNUM-07 | a non-integral value is displayed with its decimal part | `test_non_integral_value_keeps_its_decimal_part` |

### HMDT — `md_table.py`

Reading markdown tables. Nine scripts across the repo carry their own copy of this parsing; this is
the one implementation. Rows keep their source line number, so a validator can point a human at the
line that needs fixing.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HMDT-01 | a pipe-delimited row splits into stripped cell values | `test_row_splits_into_stripped_cells` |
| HMDT-02 | the leading and trailing pipes are not returned as cells | `test_outer_pipes_are_not_cells` |
| HMDT-03 | an empty cell is preserved as an empty string, not dropped | `test_empty_cell_is_preserved` |
| HMDT-04 | a dashes-only row is recognised as the separator under a table header | `test_separator_row_is_recognised` |
| HMDT-05 | a row of real content is not mistaken for a separator | `test_content_row_is_not_a_separator` |
| HMDT-06 | the rows under a heading are returned, header row first | `test_rows_are_returned_header_first` |
| HMDT-07 | the separator row is not returned as data | `test_separator_row_is_not_returned` |
| HMDT-08 | each row carries its 1-based source line number | `test_each_row_carries_its_source_line_number` |
| HMDT-09 | reading stops at the next heading | `test_reading_stops_at_the_next_heading` |
| HMDT-10 | an absent heading yields no rows | `test_absent_heading_yields_no_rows` |
| HMDT-11 | the heading is matched case-insensitively, on a substring | `test_heading_matches_case_insensitively_on_a_substring` |
| HMDT-12 | prose between the heading and the table is skipped | `test_prose_between_heading_and_table_is_skipped` |

### HUS — `uoc_sections.py`

Which UoC **sections** a Topic teaches (not which items), mapped to the institutional Delivery Mapping
vocabulary. Deliberately narrow: the docx column is a five-value dropdown, so no range expansion or
unit inheritance is needed — that machinery already exists in `validate_at_traceability.resolve_tags`
and is not duplicated here.

`taught_block(text)` — the taught/developed portion of a `coverage.md`.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HUS-01 | the block runs from the UoC-mapping heading to the next `##` heading | `test_block_runs_from_mapping_heading_to_next_h2` |
| HUS-02 | an "applied earlier / elsewhere" marker truncates the block | `test_applied_earlier_marker_truncates_the_block` |
| HUS-03 | content before the mapping heading is excluded | `test_content_before_the_mapping_heading_is_excluded` |
| HUS-04 | an absent mapping heading yields an empty block | `test_absent_mapping_heading_yields_an_empty_block` |

`sections_taught(text)` — the section codes tagged within that block.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HUS-05 | a section code is collected from a canonical unwrapped tag | `test_section_is_collected_from_a_canonical_tag` |
| HUS-06 | a backtick-wrapped tag is not counted — the canonical form is unwrapped | `test_wrapped_tag_is_not_counted` |
| HUS-07 | a section appearing many times is reported once | `test_repeated_section_is_reported_once` |
| HUS-08 | tags outside the taught block are not counted | `test_tags_outside_the_taught_block_are_not_counted` |
| HUS-09 | a line carrying no tag contributes nothing | `test_line_without_a_tag_contributes_nothing` |
| HUS-10 | a malformed bracket is ignored rather than raising | `test_malformed_bracket_is_ignored` |

`to_delivery_mapping(sections)` — our section codes as the template's dropdown values.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HUS-11 | `PC` maps to `PC` | `test_pc_maps_to_pc` |
| HUS-12 | `KE` maps to `Know` | `test_ke_maps_to_know` |
| HUS-13 | `PE` and `FS` both map to `Skill` | `test_pe_and_fs_both_map_to_skill` |
| HUS-14 | `AC` maps to `Cond` | `test_ac_maps_to_cond` |
| HUS-15 | the result is de-duplicated and in a stable order | `test_result_is_deduplicated_and_stably_ordered` |
| HUS-16 | a section with no institutional equivalent is dropped | `test_section_with_no_institutional_equivalent_is_dropped` |

### HDT — `docx_template.py`

Filling an **institutional** template — a document someone else designed, whose formatting must
survive. Distinct from `scripts/helpers/docx_tables.py`, which *builds* branded tables from nothing:
there the styling is ours to set, here it is theirs to preserve.

`clone_block_after(paragraph, table)` — repeat a heading-plus-table unit.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HDT-01 | the document gains one paragraph and one table | `test_document_gains_one_paragraph_and_one_table` |
| HDT-02 | the clone sits immediately after the source table in document order | `test_clone_sits_immediately_after_the_source_table` |
| HDT-03 | the clone's paragraph carries the same text as the source | `test_clone_paragraph_carries_the_same_text` |
| HDT-04 | the clone's table has the same row and column count as the source | `test_clone_table_has_the_same_shape` |
| HDT-05 | editing the clone leaves the source untouched | `test_editing_the_clone_leaves_the_source_untouched` |

`set_cell_text(cell, text)` — write a value into a template cell, keeping the template's formatting.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HDT-06 | the cell reads back the value written | `test_cell_reads_back_the_value_written` |
| HDT-07 | the existing run's formatting survives the write | `test_existing_run_formatting_survives_the_write` |
| HDT-08 | a cell with no runs yet can still be written to | `test_cell_with_no_runs_can_still_be_written` |
| HDT-09 | a multi-line value becomes one paragraph per line | `test_multiline_value_becomes_one_paragraph_per_line` |
| HDT-10 | writing replaces the previous content rather than appending to it | `test_writing_replaces_rather_than_appends` |

`ensure_row_cells(row, n)` — a supplied template may ship rows narrower than its own header.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HDT-11 | a row shorter than the header gains cells until it matches | `test_narrow_row_gains_cells_until_it_matches` |
| HDT-12 | a row already wide enough is left untouched | `test_wide_enough_row_is_untouched` |
| HDT-13 | added cells copy the formatting of the row's last cell | `test_added_cells_copy_the_last_cells_formatting` |

`set_cell_block(cell, blocks)` — write real content where the template held a styled placeholder.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HDT-14 | each block becomes its own paragraph, in order | `test_each_block_becomes_its_own_paragraph` |
| HDT-15 | a block marked as a heading is bold | `test_heading_block_is_bold` |
| HDT-16 | a block not marked as a heading is not bold | `test_non_heading_block_is_not_bold` |
| HDT-17 | filled content is explicitly black, overriding any colour the placeholder's **style** carries | `test_placeholder_colour_is_cleared` |
| HDT-18 | `set_cell_text` removes any content control the cell held — a filled cell must not still offer its dropdown | `test_writing_removes_a_content_control` |
| HDT-22 | `set_cell_block` removes it too | `test_writing_a_block_removes_a_content_control` |
| HDT-19 | a cell wrapped in a content control is promoted to a real cell on its row | `test_wrapped_cell_is_promoted_to_a_real_cell` |
| HDT-20 | promoting leaves the row's cells in their original left-to-right order | `test_promoting_preserves_left_to_right_order` |
| HDT-21 | a row whose cells are all wrapped ends up with every cell writable | `test_every_cell_is_writable_after_promoting` |

### HLLN — `lln_requirements.py`

The institutional LLN section, derived from the units' own Foundation Skills rather than written by
hand. Only the **LLN-relevant** skills count: a unit's Foundation Skills also cover planning, problem
solving and self-management, which are not language, literacy or numeracy demands.

Cross-process by nature: the source is extraction's `consolidated_uoc.md`; the consumer is a delivery
document. Lives in `common/` for that reason.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HLLN-01 | a Reading skill is collected under the reading heading | `test_reading_is_collected` |
| HLLN-02 | an Oral communication skill is collected under the language heading | `test_oral_communication_is_collected` |
| HLLN-03 | a Writing skill is collected under the writing heading | `test_writing_is_collected` |
| HLLN-04 | a Numeracy skill is collected under the numeracy heading | `test_numeracy_is_collected` |
| HLLN-05 | Planning and organising is excluded — not an LLN demand | `test_planning_and_organising_is_excluded` |
| HLLN-06 | Problem solving and Self-management are excluded | `test_problem_solving_and_self_management_are_excluded` |
| HLLN-07 | skills from every unit in the cluster are amalgamated under one heading | `test_skills_from_every_unit_are_amalgamated` |
| HLLN-08 | an item repeated verbatim across units is listed once | `test_item_repeated_across_units_is_listed_once` |
| HLLN-09 | the trailing source-unit tag is stripped from the item text | `test_source_unit_tag_is_stripped` |
| HLLN-10 | headings are emitted in the institution's order, and an empty heading is omitted | `test_headings_are_ordered_and_empty_ones_omitted` |
| HLLN-11 | rendering produces one bullet per item beneath each heading | `test_rendering_produces_one_bullet_per_item` |
| HLLN-12 | a bullet joining two demands with `<br>` becomes two separate items | `test_br_joined_demands_become_separate_items` |
| HLLN-13 | no markup survives into a demand — the guard against the next tag the source uses | `test_no_markup_survives_into_a_demand` |

### CDP — delivery step 06, `validate_cluster_delivery_plan.py`

The Step-6 gate: a **completeness-for-generation** check on a cluster's `delivery/delivery-plan.md`. A
PASS means the outline holds every decision the docx generator needs; each failure names a decision still
to be made. It does **not** judge whether the sequence is good — that stays the human's call.

Invocation and contract resolution. The two path flags locate **one cluster's** plan; the
whole-of-semester plan is step 07's separate `validate_semester_delivery_plan.py`.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| CDP-01 | `--plan` names the outline file directly | `test_plan_flag_names_the_file_directly` |
| CDP-02 | `--cluster-dir` reaches the same file by appending `delivery/delivery-plan.md` — a path convenience, not a different scope | `test_cluster_dir_flag_reaches_the_same_file` |
| CDP-03 | a plan file that does not exist fails with a message naming the path | `test_missing_plan_file_fails_naming_the_path` |
| CDP-04 | a format document that cannot be located fails, telling the user to pass `--format` | `test_unlocatable_format_doc_fails_telling_you_to_pass_it` |
| CDP-05 | a format document with no `## Skeleton` block fails, naming the document | `test_format_doc_without_a_skeleton_fails` |

Contract structure — driven by the skeleton, not hard-coded.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| CDP-06 | a plan with no `# … Delivery Plan` title fails | `test_missing_title_fails` |
| CDP-07 | a plan with no `> **INSTANCE:** …` banner fails | `test_missing_instance_banner_fails` |
| CDP-08 | a heading named in the skeleton but absent from the plan fails, naming the heading | `test_missing_heading_fails_naming_it` |
| CDP-09 | a header field named in the skeleton but absent from the plan fails, naming the field | `test_missing_header_field_fails_naming_it` |
| CDP-10 | a header field that is present but has an empty value fails | `test_empty_header_field_fails` |
| CDP-11 | a grid column named in the skeleton but absent from the plan's table fails, naming the column | `test_missing_grid_column_fails_naming_it` |

Grid consistency.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| CDP-12 | a complete, internally consistent plan passes with exit 0 | `test_complete_consistent_plan_passes` |
| CDP-13 | an empty cell in any required column fails as undecided | `test_undecided_cell_fails` |
| CDP-14 | a blank `Placed` cell fails — an intentionally empty session must be written `—` | `test_blank_placed_cell_fails` |
| CDP-15 | a `Mode` outside `{online, classroom}` fails, listing the permitted values | `test_invalid_mode_fails_listing_permitted_values` |
| CDP-16 | an `Activity` outside the seven permitted values fails, listing them | `test_invalid_activity_fails_listing_permitted_values` |
| CDP-17 | a gap in the session numbering fails, naming the missing number | `test_gap_in_session_numbering_fails` |
| CDP-18 | a duplicated session number fails, naming the duplicate | `test_duplicate_session_number_fails` |

Placement coverage — every built Topic and every assessment must appear somewhere in the grid.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| CDP-19 | a built Topic placed in no session fails, naming the Topic | `test_unplaced_topic_fails_naming_it` |
| CDP-20 | an assessment placed in no session fails, naming the assessment | `test_unplaced_assessment_fails_naming_it` |
| CDP-21 | a zero-padded reference (`T01`) satisfies Topic 1 — padding is not a gap | `test_zero_padded_topic_reference_counts_as_placed` |
| CDP-22 | a cluster with no built Topics warns rather than fails — there is nothing to place | `test_no_built_topics_warns_rather_than_fails` |

Dates — derived from the intake's start date, teaching days and class times, but still checked: a
wrong date silently produces a document scheduling a session on a day that does not exist.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| CDP-28 | a `Date` that is not ISO `YYYY-MM-DD` fails, naming the offending value | `test_non_iso_date_fails_naming_the_value` |
| CDP-29 | session dates that go backwards fail — sessions run forward in time | `test_dates_going_backwards_fail` |

Frame reconciliation — against the sibling `cluster-specification.md`.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| CDP-23 | a grid row count differing from `Total sessions available` fails | `test_row_count_differing_from_declared_total_fails` |
| CDP-24 | a frame budgeting an onboarding session, with none in the grid, fails | `test_budgeted_onboarding_missing_from_grid_fails` |
| CDP-25 | a frame budgeting a spare session, with none in the grid, fails | `test_budgeted_spare_missing_from_grid_fails` |
| CDP-26 | an intake total differing from the frame's nominal total is **reported, not failed** — it is the intake's real allocation | `test_intake_total_differing_from_frame_is_reported_not_failed` |
| CDP-27 | a missing `cluster-specification.md` warns rather than fails, and reconciliation is skipped | `test_missing_cluster_specification_warns_rather_than_fails` |

### CDG — delivery step 06, `build_cluster_delivery_plan.py`

Fills the institutional `Delivery_Plan_Template_v0.1.docx` from a **validated** outline. The template
ships with three session blocks; a real intake needs one per session, so blocks are cloned. Everything
written is derived — nothing is invented and nothing is asked for a second time.

Refusing to run.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| CDG-01 | an outline that does not pass the step-6 gate is refused, and the reason reported | `test_invalid_outline_is_refused` |
| CDG-02 | the source template is left unmodified on disk | `test_source_template_is_not_modified` |

Session blocks.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| CDG-03 | the document carries exactly one session block per grid row | `test_one_session_block_per_grid_row` |
| CDG-04 | session blocks appear in grid order | `test_session_blocks_appear_in_grid_order` |
| CDG-05 | each block's Session date is the row's `Date` | `test_session_date_comes_from_the_date_column` |
| CDG-06 | each block's Time is the row's `Time` | `test_time_comes_from_the_time_column` |

Translation into the institution's vocabulary.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| CDG-07 | `online` becomes `O` and `classroom` becomes `FTF` in the Delivery column | `test_mode_is_translated_to_institutional_codes` |
| CDG-08 | an assessment session carries its AT's declared assessment type | `test_assessment_session_carries_its_declared_type` |
| CDG-09 | a session running no assessment leaves the Assessment column empty | `test_non_assessment_session_leaves_assessment_empty` |
| CDG-10 | the Delivery Mapping column carries the sections the placed Topic teaches | `test_delivery_mapping_carries_the_topics_sections` |
| CDG-11 | a session placing nothing has an empty Delivery Mapping | `test_session_placing_nothing_has_empty_mapping` |

Content and fidelity.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| CDG-12 | the Topic and description column names what the session runs, by title — `Topic 01 — Web-scale architecture design`, not `T1` | `test_topic_column_names_what_the_session_runs` |
| CDG-20 | a Topic whose `coverage.md` has no readable title falls back to its plain reference | `test_topic_without_a_title_falls_back_to_its_reference` |
| CDG-21 | a session running an assessment names the assessment by title — `AT1 — Cloud Expansion: Design & DR Plan` | `test_assessment_session_names_the_assessment` |
| CDG-22 | an assessment with no readable title in the assessment plan falls back to its plain reference | `test_assessment_without_a_title_falls_back_to_its_reference` |
| CDG-23 | a session placing nothing is labelled by its Activity — a `spare` session reads as spare, not as a blank row | `test_spare_session_is_labelled_spare` |
| CDG-24 | the Activity label is only used when nothing is placed — it never displaces a Topic or assessment | `test_activity_label_never_displaces_placed_content` |
| CDG-13 | the template's own cell formatting survives being filled | `test_template_cell_formatting_survives` |
| CDG-14 | the document is written to the path asked for | `test_document_is_written_where_asked` |
| CDG-15 | a session block keeps only the data rows it fills — the template's spare rows are removed | `test_unused_template_rows_are_removed` |

Document header — the three fillable tables above the session blocks.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| CDG-16 | the Details table carries the qualification, unit and cohort values from the outline | `test_details_table_carries_qualification_unit_and_cohort` |
| CDG-17 | the Materials and Resources table carries the outline's materials value | `test_materials_table_carries_the_materials_value` |
| CDG-18 | the LLN table carries requirements derived from the cluster's own units | `test_lln_table_carries_the_requirements_value` |
| CDG-19 | changing the units changes the generated LLN — a derivation cannot go stale | `test_changing_the_units_changes_the_generated_lln` |

## Open decisions

Collect unresolved cases here, and mark the case itself. An unresolved case does not pass — resolve it
before the plan is green.

- [none yet]
