
# BusinessObjects XI R2 constants

# I don't use these yet -- they're here for future reference

# alignment_type = { 'horizontal', 'indent', 'row_by_row_autofit', 'text_wrap', 'vertical'  }
cardinality = { 0:'Unknown', 1:'OneToOne', 2:'OneToMany', 3:'ManyToOne', 4:'ManyToMany' }
column_key = { 0:'Unknown', 1:'All', 2:'None', 3:'Primary', 4:'Secondary', 5:'Extern' }
column_type = { 0:'Null', 1:'Numeric', 2:'Character', 3:'Date', 4:'Text', 5:'Unknown' }
connection_state = { 1:'KeepActiveWholeSession', 2:'KeepActiveForxx', 3:'DisconnectAfterEachTransaction' }
connection_type = { 1:'Personal', 2:'Secured', 3:'Shared' }
object_aggregate = { 1:'Sum', 2:'Max', 3:'Min', 4:'Avg', 5:'Count', 6:'Null' }
object_qualification = { 1:'Dimension', 2:'Detail', 3:'Measure' }
object_security_access = { 0:'Public', 1:'Controlled', 2:'Restricted', 3:'Confidential', 4:'Private' }
object_type = { 0:'Null', 1:'Numeric', 2:'Character', 3:'Date', 4:'Blob', 5:'Unknown' }
outer_join = { 1:'None', 2:'Left', 3:'Right', 4:'Full' }
variable_type = { 1:'String', 2:'Numeric', 3:'Date' }

#
# attribute - name, parent, value (string)
#
# class - attributes, classes, description, name, objects, parent, predefined_conditions, root_class, show (boolean)
#
# column - key (column_key), name, parent, type (column_type)
#
# condition (aka predefined condition) - attributes, description, name, 
#    parent, root_class, show, tables, where
#
# connection - active_state (connection_state), active_time (long), 
#    array_bind_size (long), array_fetch_size (long), CUID (string), 
#    db_engine, db_source, is_async_mode, login_timeout (long), name, 
#    network_layer, password, perform_cost_estimate (boolean), 
#    server (string), type (connection_type), username, 
#    use_singlesignon (boolean)
#
# context - description, joins, name, parent
#
# control_option - cost_estimate_exceeded_value (long), limit_execution_time (bool),
#    limit_execution_time_value (long), limit_size_of_long_text_object (bool),
#    limit_size_of_long_text_object_value (long), limit_size_of_result_set (bool),
#    limit_size_of_result_set_value (long), parent, warn_if_cost_estimate_exceeded (bool)
#
# custom_hierarchy, default_hierarchy - dimensions, name, parent
#
# format - alignment (alignment_type), font, number_format (string), parent
#
# font - bold (bool), color (long), italic (bool), name, parent, size (long), 
#    strikethrough (bool), underline (bool)
#
# join - cardinality, expression, first_columns, first_table, outer_join, 
#        parent, second_columns, second_table, is_shortcut
#
# key - is_enabled, parent, select (string), type (column_key?)
#
# linked_universe - description, fullname, longname, name, parent
#
# list_of_values - name, parent, values
#
# object - active_month (bool), active_quarter (bool), active_year (bool), aggregate_function (object_aggregate), 
#    allow_user_to_edit_lov (bool), associated_dimension (object), attributes, 
#    autorefresh_lov_beforeuse (bool), can_be_used_condition (bool), can_be_used_result (bool), 
#    can_be_used_sort (bool), db_format (string), description, export_lov_with_universe (bool), 
#    format, has_lov, keys, list_of_values, month_name (string), name, objects, 
#    parent, qualification (object_qualification), quarter_name (string), root_class, 
#    security_access_level (object_security_access), select, show (bool), tables, type (object_type), 
#    use_hierarchical_display (bool), where, year_name (string)
#
# object_strategy - help (string), name, parent
#
# parameter - name, parent, value
#
# sql_option - complex_operators, multiple_sql_for_context, 
#    multiple_sql_for_measure, operators, parent, prevent_cartesion_products,
#    select_multiple_contexts, subqueries
#      (all except parent are booleans)
# 
# table - columns, incompatible_objects, incompatible_predefined_conditions,
#    is_alias, is_derived, name, original_table (table), parent, 
#    sql_of_derived_table (string), sql_of_derived_table_with_alias (string), 
#    weight (long), xpos (long), ypos (long)
#
# universe - author, candidate_classes, candidate_joins, classes, comments,
#    connection, contexts, control_option, creation_date, current_join_strategy,
#    current_object_strategy, current_owner, current_qualifier, 
#    current_table_strategy, custom_hierarchies, db_tables, default_hierarchies,
#    description, fullname, joins, join_strategies, language, linked_universes,
#    long_name, modification_date, modifier (string), name, object_strategies, owners,
#    owner_supported, parameters, parent, path, qualifiers, qualifier_supported,
#    saved, sql_option, tables, table_strategies, use_custom_hierarchies, windows
#
# variable - interpert_as (variable_type), is_multi_valued, name, parent, value (string)
#