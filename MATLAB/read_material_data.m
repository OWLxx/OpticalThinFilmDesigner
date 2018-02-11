

%## Author: David Klotzkin
%# Give a list of names of material (SiN, TiO2, SiO2) it creates 
%#arrays in order (1 for SiN, 2 for TiO2, 3 for SiO2) of the format
%# lambda, n, k, where lambda, matches with the index to be used

function [indexesarray] = read_material_data(filename)
    
    global lambda_min;
    global lambda_max;
    global lambda_step;
    if filename(end-2)~='t' || filename(end-1)~='x' || filename(end)~='t'
         filename=strcat(filename,'.txt');
    end
            temp=importdata(filename,'\t'); % read into tempdata
            tempdata = temp.data;
            targetlambda=lambda_min;  % what do we wnat teh first array entry to beep
            n=0;
            k=0;
            lambda=0;
            linenum=1;
            [tempr,tempc]=size(tempdata);
            if tempc~=3
                tempdata(:,3)=zeros(tempr,1);
            end
            for jj=1:size(tempdata(:,1))  % parse through line by line, create new array, properly interpolated
                % dang it, I actually don't need to go through all the data table - I just need to go to the
                %lambda max but not statemetn I can write here seems to be working  I will look into it later
                
                oldlambda=lambda;
                oldn=n;
                oldk=k;
                lambda=tempdata(jj, 1); % find current lambda, n, k
                n=tempdata(jj,2);
                k=tempdata(jj,3);
                
                while ((targetlambda<=lambda)&&(targetlambda<=lambda_max))

                    %we have a new entry into our table
                    indexesarray(linenum,1)= oldn+(n-oldn)/(lambda-oldlambda)*(targetlambda-oldlambda);  %linearly interpolate n
                    indexesarray(linenum,2)= oldk+(k-oldk)/(lambda-oldlambda)*(targetlambda-oldlambda);
                    
%                     indexesarray(linenum,1)=targetlambda; %for debugging
                    linenum=linenum+1;
                    targetlambda=targetlambda+lambda_step;  
                        
                end
                % here, do interpolation as appropriate to create the correct index arrayfun
          
            end
          indexesarray(indexesarray<0)=0;
end
   
          

