    <%page args="universe"/>
    Universe Manifest
        <% parms = universe.parameters %>
        ${parms.universe_name} (${parms.universe_filename}.unv)
        Revision ${parms.revision}

        Description: ${parms.description}
        Comments: ${parms.comments}
        Created by: ${parms.created_by} on ${parms.created_date}
        Modified by: ${parms.modified_by} on ${parms.modified_date}
        
        Domain: ${parms.domain}
        Database engine: ${parms.dbms_engine}
        Network layer: ${parms.network_layer}

    Strategies

        Object strategy: ${parms.object_strategy}

    Controls

        Query time limit: ${parms.query_time_limit} minutes
        Query row limit: ${parms.row_limit} rows
        Cost estimate warning limit: ${parms.cost_estimate_warning_limit} minutes
        Long text limit: ${parms.long_text_limit} characters

    SQL Parameters

    % for name, value in universe.custom_parameters.items():
        ${name} = ${value}
    % endfor

    Links
    
        (pyunv does not support links yet)

    Objects
    % for uclass in universe.classes:
        ${write_class_objects(uclass, 1)} \
    % endfor
    <%def name="write_class_objects(uclass, level)">
        ${uclass.name}
        % for obj in uclass.objects:
            ${obj.name}   id: ${obj.id_}, visible: ${obj.visible}, description: ${obj.description}, select: ${obj.select_sql}, where: ${obj.where_sql}
        % endfor
		<% level = level+1 %> \
		% for subclass in uclass.subclasses:
		    ${write_class_objects(subclass, level)} \
		% endfor
    </%def>
    Conditions
    % for uclass in universe.classes:
        ${write_class_conditions(uclass, 1)} \
    % endfor
    <%def name="write_class_conditions(uclass, level)">
        ${uclass.name}
        % for condition in uclass.conditions:
            ${condition.name}   id: ${condition.id_}, description: ${condition.description}, where: ${condition.where_sql}
        % endfor
		<% level = level+1 %> \
		% for subclass in uclass.subclasses:
		    ${write_class_conditions(subclass, level)} \
		% endfor
    </%def>
    Hierarchies
    
        (pyunv does not support hierarchies yet)

    Tables

    % for table in universe.tables:
        ${table.name}   id: ${table.id_}
    % endfor

    Columns
    
    % for column in universe.columns:
        ${column.fullname}   id: ${column.id_}
    % endfor

    Joins

    % for join in universe.joins:
        ${join.statement}   id: ${join.id_} 
    % endfor
    
    Contexts
    
    % for c in universe.contexts:
        ${c.name}   id: ${c.id_}, description: ${c.description}, joins: ${c.join_list} 
    % endfor
