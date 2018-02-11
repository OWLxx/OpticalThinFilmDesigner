function handles=plotdata(handles)
global lambda_min;
global lambda_max;
cla(handles.axes1);
temp=importdata(get(handles.lr,'String'));
tempdata=temp.data;
[handles.wavm,pos]=sort(tempdata(:,1));
reftemp=tempdata(pos,2);
if sum(cell2mat(strfind(temp.textdata,'T')))==0  % note there
    handles.refm=reftemp;
else
    handles.refm=100-reftemp;
end
axes(handles.axes1);
handles.pm=plot(handles.wavm,handles.refm,'y');
set(gca,'xlim',[lambda_min lambda_max]);


end

