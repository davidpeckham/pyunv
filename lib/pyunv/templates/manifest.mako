## -*- coding: utf-8 -*-
    <%page args="universe"/>
    Universe Manifest
        <% parms = universe.parameters %>
        ${parms.universe_name} (${parms.universe_filename}.unv)
        Revision ${parms.revision}

        Description: ${parms.description}
        Comments: ${parms.comments}
        Created by: ${parms.created_by} on ${parms.created_date}
        Modified by: ${parms.modified_by} on ${parms.modified_date}

    Parameters

        Query time limit: ${parms.query_time_limit} minutes
        Query row limit: ${parms.row_limit} rows
        Object strategy: ${parms.object_strategy}
        Cost estimate warning limit: ${parms.cost_estimate_warning_limit} minutes
        Long text limit: ${parms.long_text_limit} characters
        Domain: ${parms.domain}
        Database engine: ${parms.dbms_engine}
        Network layer: ${parms.network_layer}

    Source Tables

    % for table in universe.tables:
        ${table.name} (id ${table.id_})
    % endfor

    Source Columns
    
    % for column in universe.columns:
        ${column.table_name}.${column.name} (id ${column.id_})
    % endfor

    Joins

    % for join in universe.joins:
        ${join.name} (id ${join.id_})
    % endfor
	<%doc>
    Class Index
    % for uclass in universe.classes:
        ${write_class_summary(uclass, 1)}
    % endfor

    <%def name="write_class_summary(uclass, level)">
        ${uclass.name}
        <% level = level+1 %>
        % if level < 6:
            % for subclass in uclass.subclasses:
                ${write_class_summary(subclass, level)}
            % endfor
        % endif
    </%def>
	</%doc>

    Classes
    % for uclass in universe.classes:
        ${write_class(uclass, 1)}
    % endfor
    <%def name="write_class(uclass, level)">
        ${uclass.name}
        % for obj in uclass.objects:
            ${obj.name}  description: ${obj.description}, select: ${obj.select_sql}, where: ${obj.where_sql}
        % endfor
        % for condition in uclass.conditions:
            ${condition.name}  description: ${condition.description}, where: ${condition.where_sql}
        % endfor
        <% level = level+1 %> \
		% for subclass in uclass.subclasses:
		    ${write_class(subclass, level)}
		% endfor
    </%def>
