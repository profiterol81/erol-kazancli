function out = arffparser(fileName)
   
    try
        if isempty(strfind(fileName, '.arff'))
            
            fileName = [fileName '.arff'];
        
        end

        fid = fopen(fileName, 'r');

        if fid == -1
            error('ERROR:ARFFPARSER', 'File could not be opened')
        end

    catch ME
        error('ERROR:ARFFPARSER', 'File not found');
    end

    % Read the file
    theText = textscan(fid, '%s', 'delimiter', '\n');
    theText = theText{1};

    % Remove empty lines
    theText = theText(~cellfun(@isempty, theText));

    % Make all letters low case
    theText = lower(theText);

    % Check if there is a relation naming in the arff file
    if isempty(strfind(theText, '@relation'))
        error('ERROR:ARFFPARSER', ...
            'Not valid relation naming in .arff file');
    end

    % Get only the lines after the relation declaration
    theText = theText(find(~cellfun(@isempty, ...
        strfind(theText, '@relation')) == 1) : length(theText));

    tmpVar = {};

    % Strip off comments
    for indx = 1:length(theText)
        tmpVar2 = theText{indx};
        if ~strcmp(tmpVar2(1), '%')
            tmpVar{length(tmpVar) + 1, 1} = tmpVar2;
        end
    end

    theText = tmpVar;

    clear tmpVar;

    % Break up the text in two regions
    textAttr = theText(2:( find(~cellfun(@isempty, ...
        strfind(theText, '@data')) == 1) - 1));

    textVals = theText(( find(~cellfun(@isempty, ...
        strfind(theText, '@data')) == 1) +1):length(theText));

    % Close the file
    fclose(fid);

    % Clear unwanted variables
    clear theText;
    clear fid;

    % For each line of the attributes text
    for indx = 1:length(textAttr)

        % Get the kind of the attribute based on the ending latter
        endingLetter = textAttr{indx}(length(textAttr{indx}));

        % Find the starting index of the attribute's name and values
        % (if any)

        % Numeric or real attributes
        isInteger = false;
        if strcmp(endingLetter, 'c') || strcmp(endingLetter, 'l') || strcmp(endingLetter, ']') 

            % Get the defined kind
            if strcmp(endingLetter, 'l')
                nameStr = 'real';
            elseif strcmp(endingLetter, ']')
                nameStr = 'integer';
                isInteger = true;
            else    
                nameStr = 'numeric';
            end                

            % Assing values, treating real as numeric
            theKind = 'numeric';
            strKind = 'numeric';

            % Assign indices
            if isInteger
                indxEnd = strfind(textAttr{indx}, 'integer') - 1; 
                indxStart = length('@attribute') + 1;
                rangeStr = textAttr{indx}(indxEnd:length(textAttr{indx}));
                rangeStart = strfind(rangeStr, '[') + 1;
                rangeEnd = strfind(rangeStr, ']') - 1;
                rangeStr = rangeStr(rangeStart:rangeEnd);
                minMax = strsplit(rangeStr, ',');
                min = cell2mat(minMax(1));
                max = cell2mat(minMax(2));
            else 
                indxEnd = length(textAttr{indx}) - length(nameStr);
                indxStart = length('@attribute') + 1;
            end

            % Clear unwanted variables
            clear nameStr;

        elseif strcmp(endingLetter, '}') % Nominal attributes

            % Indicate the kind of the attribute
            theKind = 'nominal';

            % Find the values for the nominal attribute
            indxEnd = strfind(textAttr{indx}, '}') - 1;
            indxStart = strfind(textAttr{indx}, '{') + 1;
            strKind = textAttr{indx};
            strKind = strKind(indxStart:indxEnd);

            % Find the indices for the name of the attribute
            indxStart = length('@attribute') + 1;
            indxEnd = strfind(textAttr{indx}, '{') - 1;

        elseif strcmp(endingLetter, 'g') % String attributes

            strKind = 'string';
            indxEnd = length('string') + 1;
            indxStart = length('@attribute ') + 1;

        elseif strcmp(endingLetter, 'e') % Date attributes

            theKind = 'date';
            strKind = 'date';
            indxEnd = length('date') + 1;
            indxStart = length('@attribute ') + 1;

        else

            q = 'No appropriate kind of attribute';
            error('ERROR:ARFFPARSER',q)

        end

        % Clear unwanted variables
        clear endingLetter;

        % Get the current string
        tmpStr = textAttr{indx};

        % Check for spaces and make indices point to no space chars
        while isspace(tmpStr(indxStart))
            indxStart = indxStart + 1;
        end

        while isspace(tmpStr(indxEnd))
            indxEnd = indxEnd - 1;
        end

        % Check if there are any quote marks and remove them
        if strcmp(textAttr{indx}(indxStart), '"') || ...
                strcmp(textAttr{indx}(indxStart), '''')

            % And if it is increase the index for starting of the name
            indxStart = indxStart +1;
        end

        if strcmp(textAttr{indx}(indxEnd), '"') || ...
                strcmp(textAttr{indx}(indxEnd), '''')

            % And if it is decrease the index for ending of the name
            indxEnd = indxEnd - 1;
        end            

        % Get the name of the attribute
        strName = textAttr{indx}(indxStart:indxEnd);

        % Remove spaces from name
        strName = strName(~isspace(strName));

        % Remove punctuation chars
        strName(isstrprop(strName, 'punct')) = [];

        % Remove non alphanumeric chars
        strName(~isstrprop(strName, 'alphanum')) = '_';

        % Add the attribute to the output struct
        if strcmp(theKind, 'numeric')
            try
                eval(['out.' strName '.kind =''' strKind ''';']);
            catch me
                disp('OK')
            end
        elseif strcmp(theKind, 'nominal')
            if isstrprop(strKind(1), 'digit')
                eval(['out.' strName '.kind = [str2num(strKind)];']);
            else

                % Check if there are single quotes for the string
                % argument

                % Check if the first character is singe quote
                if ~strcmp(strKind(1), '''')
                    strKind = ['''' strKind];
                end

                % Then check position of commas
                commaInds = strfind(strKind, ',');

                % Then check for the rest characters and insert single
                % quote wherever is needed
                for indx2 = 1:length(commaInds)

                    if ~strcmp(strKind(commaInds(indx2) - 1), '''')

                        strKind = [strKind(1:commaInds(indx2)-1) ...
                            '''' strKind(commaInds(indx2):...
                            length(strKind))];

                        % If something is inserted, get again the
                        % position of commas
                        commaInds = strfind(strKind, ',');

                    end

                    if ~strcmp(strKind(commaInds(indx2) + 1), '''')

                        strKind = [strKind(1:commaInds(indx2)) ...
                            '''' strKind(commaInds(indx2) + 1:...
                            length(strKind))];

                        % If something is inserted, get again the
                        % position of commas
                        commaInds = strfind(strKind, ',');

                    end

                end

                % Then check for the last one
                if ~strcmp(strKind(length(strKind)), '''')
                    strKind = [strKind ''''];
                end

                try
                    eval(['out.' strName '.kind = {' strKind '};']);
                catch me
                    disp('OK')
                end
            end
        end

        % Check the values' kind of the current attribute
        if strcmp(theKind, 'numeric')

            kindType = 'digit';
            tmpVal = [];

        elseif strcmp(theKind, 'nominal')

            tmpStr = textVals{1};
            commaInds = strfind(tmpStr, ',');

            switch indx
                case 1
                    tmpStrIndx = 1;
                case length(textAttr)
                    tmpStrIndx = commaInds(length(commaInds)) + 1;
                otherwise
                    tmpStrIndx = commaInds(indx-1) + 1;
            end

            if isstrprop(tmpStr(tmpStrIndx), 'alpha') || ...
                    isstrprop(tmpStr(tmpStrIndx), 'punct')
                kindType = 'string';
                tmpVal = {};
            elseif isstrprop(tmpStr(tmpStrIndx), 'digit')
                kindType = 'digit';
                tmpVal = [];
            end

        elseif strcmp(theKind, 'date')

            kindType = 'string';
            tmpVal = {};

        elseif strcmp(theKind, 'string')

            kindType = 'string';
            tmpVal = {};

        end

        % Get the values for that attribute
        for indx2 = 1:length(textVals)

            % Get the instance string in a variable
            tmpStr = textVals{indx2};

            % Remove spaces (if any)
            tmpStr = tmpStr(~isspace(tmpStr));

            % Remove commas taken as strings (in single or double
            % quotes, e.g. , 'a string, with a comma' or "a string,
            % with a comma"
            foundSingleQuote = false;
            for indx3 = 1:length(tmpStr)
                if strcmp(tmpStr(indx3), '''')
                    foundSingleQuote = true;
                end

                if foundSingleQuote && ...
                        strcmp(tmpStr(indx3), '''')
                    foundSingleQuote = false;
                end

                if strcmp(tmpStr(indx3), ',') && ...
                    foundSingleQuote
                    tmpStr(indx3) = '_';
                end
            end

            foundSingleQuote = false;
            for indx3 = 1:length(tmpStr)
                if strcmp(tmpStr(indx3), '"')
                    foundSingleQuote = true;
                end

                if foundSingleQuote && ...
                        strcmp(tmpStr(indx3), '"')
                    foundSingleQuote = false;
                end

                if strcmp(tmpStr(indx3), ',') && ...
                    foundSingleQuote
                    tmpStr(indx3) = '_';
                end
            end

            % Determine when a new value occurs in the string.
            % Get the positions of comma characters
            commaInds = strfind(tmpStr, ','); 

            % Read the values from the text string according to value's
            % index
            if indx == 1

                % Get from the string the first numeric variable
                tmpVal2 = tmpStr(1:commaInds(indx)-1);

                if strcmp(kindType, 'digit')

                    % Check for missing values
                    if strcmp(tmpVal2, '?')
                        tmpVal2 = 'NaN';
                    end

                    % Assing the value
                    tmpVal = [tmpVal str2num(tmpVal2)];

                elseif strcmp(kindType, 'string')

                    % Check and remove the first quote (if any)
                    if strcmp(tmpVal2(1), '''') || ...
                            strcmp(tmpVal2(1), '"')
                        tmpVal2(1) = [];
                    end

                    % Check and remove the last quote (if any)
                    if strcmp(tmpVal2(length(tmpVal2)), '''') || ...
                            strcmp(tmpVal2(length(tmpVal2)), '"')
                        tmpVal2(length(tmpVal2)) = [];
                    end

                    if strcmp(tmpVal2, '?')
                        tmpVal2 = 'NaN';
                    end

                    tmpVal{indx2} = tmpVal2;
                end
            elseif indx == length(textAttr)

                % Get from string the proper values
                tmpVal2 = tmpStr(commaInds(length(commaInds))...
                        + 1 : length(tmpStr));

                if strcmp(kindType, 'digit')

                    % Check for missing values
                    if strcmp(tmpVal2, '?')
                        tmpVal2 = 'NaN';
                    end

                    % Get from the string the last numeric variable
                    tmpVal = [tmpVal str2num(tmpVal2)];

                elseif strcmp(kindType, 'string')

                    % Check and remove the first quote (if any)
                    if strcmp(tmpVal2(1), '''') || ...
                            strcmp(tmpVal2(1), '"')
                        tmpVal2(1) = [];
                    end

                    % Check and remove the last quote (if any)
                    if strcmp(tmpVal2(length(tmpVal2)), '''') || ...
                            strcmp(tmpVal2(length(tmpVal2)), '"')
                        tmpVal2(length(tmpVal2)) = [];
                    end

                    if strcmp(tmpVal2, '?')
                        tmpVal2 = 'NaN';
                    end

                    tmpVal{indx2} = tmpVal2;
                end

            else

                % Get from string the proper values
                tmpVal2 = tmpStr(commaInds(indx-1) + 1:...
                    commaInds(indx) - 1);

                if strcmp(kindType, 'digit')

                    % Check for missing values
                    if strcmp(tmpVal2, '?')
                        tmpVal2 = 'NaN';
                    end

                    % Get from the string the appropriate numeric
                    % variable
                    tmpVal = [tmpVal str2num(tmpVal2)];

                elseif strcmp(kindType, 'string')

                    % Check and remove the first quote (if any)
                    if strcmp(tmpVal2(1), '''') || ...
                            strcmp(tmpVal2(1), '"')
                        tmpVal2(1) = [];
                    end

                    % Check and remove the last quote (if any)
                    if strcmp(tmpVal2(length(tmpVal2)), '''') || ...
                            strcmp(tmpVal2(length(tmpVal2)), '"')
                        tmpVal2(length(tmpVal2)) = [];
                    end

                    if strcmp(tmpVal2, '?')
                        tmpVal2 = 'NaN';
                    end

                    tmpVal{indx2} = tmpVal2;

                end
            end
            if isInteger
                if (str2num(tmpVal2) > str2num(max)) || (str2num(tmpVal2) < str2num(min))
                    error('ERROR:Integer Out of Range COLUMN:%d ROW:%d VALUE:%s ALLOWEDRANGE:%s - %s', indx, indx2, tmpVal2, min, max)
                end
            end  
        end 
        
        eval(['out.' strName '.values = tmpVal ;'])
    end
end