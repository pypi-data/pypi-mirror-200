function test_suite=test_moxunit_util_remove_matlab_anchor_tag
    try % assignment of 'localfunctions' is necessary in Matlab >= 2016
        test_functions=localfunctions();
    catch % no problem; early Matlab versions can use initTestSuite fine
    end
    initTestSuite;

function test_moxunit_util_remove_matlab_anchor_tag_basics
    rand_str=@()char(20*rand(1,10)+65);

    message=rand_str();
    file_name=sprintf('%s',rand_str());
    function_name=rand_str();
    file_path=fullfile(rand_str(),rand_str(),sprintf('%s.m',file_name));
    line_number=ceil(rand()*100);


    in_out1={sprintf([...
                '%s<a href="matlab:'...
                'matlab.internal.language.'...
                'introspective.errorDocCallback('...
                '''%s>%s'', ''%s'', %d)"style="font-weight:bold">'...
                '%s>%s</a>'],...
                message,file_name,function_name,file_path,line_number,...
                file_name,function_name)...
            sprintf('%s%s>%s',...
                message,file_name,function_name)};

    in_out2={sprintf([...
                    '<a href="matlab: opentoline(''%s'',%d,0)">'...
                    'line %d</a>'],...
                    file_path,line_number,line_number),...
            sprintf('line %d',line_number)};

    in_out3={moxunit_util_strjoin([in_out1(1),in_out2(1)],''),...
             moxunit_util_strjoin([in_out1(2),in_out2(2)],'')};

    in_out_cell=cat(1,in_out1,in_out2,in_out3);
    for k=3:size(in_out_cell,1)
        a=in_out_cell{k,1};
        b=in_out_cell{k,2};

        result=moxunit_util_remove_matlab_anchor_tag(a);
        assertEqual(result,b);
    end
