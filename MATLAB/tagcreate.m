function [fn,fntemp]=tagcreate(handles)
global factor;
global passband1;
global passband2;
global angle;
global Nooflayer;
temp1=get(handles.c1,'String');
temp2=get(handles.c2,'String');
temp3=get(handles.in,'String');
temp4=get(handles.s,'String');
temp5=get(handles.spec,'String');
if get(handles.checkbox8,'value')==1
    temp7='R';
else
    temp7='T';
end

if get(handles.checkbox5,'Value')~=1  %transfer function
    fntemp=strcat(num2str(angle),temp1(1:3),temp2(1:3),temp3(1:3),temp4(1:3),temp5(1:3),temp7,num2str(passband1),num2str(passband2),num2str(factor));%field name
else
    temp6=get(handles.tf,'String');
    fntemp=strcat(num2str(angle),temp1(1:3),temp2(1:3),temp3(1:3),temp4(1:3),temp5(1:3),temp6(1:3),temp7,num2str(passband1),num2str(passband2),num2str(factor));
end
if get(handles.checkbox6,'value')==1
    fntemp=strcat('s',fntemp);
else
    fntemp=strcat('ns',fntemp);
end
fntemp(ismember(fntemp,' ,.:;!'))=[];
fn=strcat(fntemp,num2str(Nooflayer));
fn(ismember(fn,' ,.:;!'))=[];

end