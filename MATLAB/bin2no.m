
function pop1=bin2no(pop)  
% convert binary to decimal
% input:  pop popsie,chromelength,Nooflayer
% output: first row is population,normalized by design requirement
% second row is layer
global t_min;
global t_max;
[sx sy sz]=size(pop);
resolution=(t_max-t_min)/(2^sy);
poptemp=zeros(sx,sz);
pop1=zeros(sx,sz);
for i=1:sz
    for j=1:sx
        for k=1:sy
            poptemp(j,i)=2^(sy-k)*pop(j,k,i)+poptemp(j,i);
        end
    end
end
for i=1:sz
    for j=1:sx
        pop1(j,i)=t_min +poptemp(j,i)*resolution;
    end
end
end