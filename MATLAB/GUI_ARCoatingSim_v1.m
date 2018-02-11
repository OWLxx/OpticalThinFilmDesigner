function varargout = GUI_ARCoatingSim_v1(varargin)
% GUI_ARCOATINGSIM_V1 MATLAB code for GUI_ARCoatingSim_v1.fig

%      GUI_ARCOATINGSIM_V1, by itself, creates a new GUI_ARCOATINGSIM_V1 or raises the existing
%      singleton*.
%
%      H = GUI_ARCOATINGSIM_V1 returns the handle to a new GUI_ARCOATINGSIM_V1 or the handle to
%      the existing singleton*.
%
%      GUI_ARCOATINGSIM_V1('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in GUI_ARCOATINGSIM_V1.M with the given input arguments.
%
%      GUI_ARCOATINGSIM_V1('Property','Value',...) creates a new GUI_ARCOATINGSIM_V1 or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before GUI_ARCoatingSim_v1_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to GUI_ARCoatingSim_v1_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help GUI_ARCoatingSim_v1

% Last Modified by GUIDE v2.5 20-Jun-2016 22:24:45

% Begin initialization code - DO NOT EDIT

gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @GUI_ARCoatingSim_v1_OpeningFcn, ...
                   'gui_OutputFcn',  @GUI_ARCoatingSim_v1_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before GUI_ARCoatingSim_v1 is made visible.
function GUI_ARCoatingSim_v1_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to GUI_ARCoatingSim_v1 (see VARARGIN)

% Choose default command line output for GUI_ARCoatingSim_v1
clc;
addpath('indexfile');
handles.output = hObject;
global runtime;
runtime=1;
set(handles.in,'String','air');
set(handles.c1,'String','ITO_upadate');
set(handles.c2,'String','xin_0407_sio2');
set(handles.s,'String','YAG');
set(handles.mint,'String','0');
set(handles.maxt,'String','100');
set(handles.nl,'String','5');
set(handles.ng,'String','10');
set(handles.minw,'String','300');
set(handles.maxw,'String','700');
set(handles.sc,'String','10');
set(handles.minp,'String','300');
set(handles.maxp,'String','700');
set(handles.w,'String','100');
set(handles.spec,'String','phosphorspectra.txt');
set(handles.tf,'String','triangle_transfer_function');
set(handles.lr,'String','sample_R%');
set(handles.re,'String','sample_recipe');
set(handles.imp,'String','air');
set(handles.imp2,'String','air');
set(handles.checkbox2,'value',1);
set(handles.checkbox5,'value',0);
set(handles.checkbox6,'value',0);
set(handles.checkbox8,'value',1);
set(handles.sen,'String','0');
% Update handles structure
guidata(hObject, handles);

% UIWAIT makes GUI_ARCoatingSim_v1 wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = GUI_ARCoatingSim_v1_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;



function in_Callback(hObject, eventdata, handles)
% hObject    handle to in (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of in as text
%        str2double(get(hObject,'String')) returns contents of in as a double
guidata(hObject, handles);


% --- Executes during object creation, after setting all properties.
function in_CreateFcn(hObject, eventdata, handles)
% hObject    handle to in (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in inb.
function inb_Callback(hObject, eventdata, handles)
% hObject    handle to inb (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
incident = uigetfile('*.txt', 'Select the txt file for the Incident');
set(handles.in, 'String', incident(1:length(incident)-4));
guidata(hObject, handles);




function c1_Callback(hObject, eventdata, handles)
% hObject    handle to c1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of c1 as text
%        str2double(get(hObject,'String')) returns contents of c1 as a double


% --- Executes during object creation, after setting all properties.
function c1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to c1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in c1b.
function c1b_Callback(hObject, eventdata, handles)
% hObject    handle to c1b (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
materialA = uigetfile('*.txt', 'Select the TEXT (n,k) file for the Material A');
set(handles.c1, 'String', materialA(1:length(materialA)-4));
guidata(hObject, handles);



function c2_Callback(hObject, eventdata, handles)
% hObject    handle to c2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of c2 as text
%        str2double(get(hObject,'String')) returns contents of c2 as a double


% --- Executes during object creation, after setting all properties.
function c2_CreateFcn(hObject, eventdata, handles)
% hObject    handle to c2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in c2b.
function c2b_Callback(hObject, eventdata, handles)
% hObject    handle to c2b (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
materialB_filename = uigetfile('*.txt', 'Select the TEXT (n,k) file for the Material A');
set(handles.c2, 'String', materialB_filename(1:length(materialB_filename)-4));
guidata(hObject, handles);



function s_Callback(hObject, eventdata, handles)
% hObject    handle to s (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of s as text
%        str2double(get(hObject,'String')) returns contents of s as a double
substrate = uigetfile('*.txt', 'Select the TEXT (n,k) file for the Material A');
set(handles.s, 'String', substrate(1:length(substrate)-4));
guidata(hObject, handles);


% --- Executes during object creation, after setting all properties.
function s_CreateFcn(hObject, eventdata, handles)
% hObject    handle to s (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in sb.
function sb_Callback(hObject, eventdata, handles)
% hObject    handle to sb (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
sb = uigetfile('*.txt', 'Select the TEXT (n,k) file for the Material A');
set(handles.s, 'String', sb(1:length(sb)-4));
guidata(hObject, handles);




function mint_Callback(hObject, eventdata, handles)
% hObject    handle to mint (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of mint as text
%        str2double(get(hObject,'String')) returns contents of mint as a double
guidata(hObject, handles);



% --- Executes during object creation, after setting all properties.
function mint_CreateFcn(hObject, eventdata, handles)
% hObject    handle to mint (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function maxt_Callback(hObject, eventdata, handles)
% hObject    handle to maxt (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of maxt as text
%        str2double(get(hObject,'String')) returns contents of maxt as a double
guidata(hObject, handles);

% --- Executes during object creation, after setting all properties.
function maxt_CreateFcn(hObject, eventdata, handles)
% hObject    handle to maxt (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function nl_Callback(hObject, eventdata, handles)
% hObject    handle to nl (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of nl as text
%        str2double(get(hObject,'String')) returns contents of nl as a double
guidata(hObject, handles);

% --- Executes during object creation, after setting all properties.
function nl_CreateFcn(hObject, eventdata, handles)
% hObject    handle to nl (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function ng_Callback(hObject, eventdata, handles)
% hObject    handle to ng (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of ng as text
%        str2double(get(hObject,'String')) returns contents of ng as a double
guidata(hObject, handles);

% --- Executes during object creation, after setting all properties.
function ng_CreateFcn(hObject, eventdata, handles)
% hObject    handle to ng (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function minw_Callback(hObject, eventdata, handles)
% hObject    handle to minw (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of minw as text
%        str2double(get(hObject,'String')) returns contents of minw as a double
guidata(hObject, handles);

% --- Executes during object creation, after setting all properties.
function minw_CreateFcn(hObject, eventdata, handles)
% hObject    handle to minw (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function sc_Callback(hObject, eventdata, handles)
% hObject    handle to sc (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of sc as text
%        str2double(get(hObject,'String')) returns contents of sc as a double
guidata(hObject, handles);

% --- Executes during object creation, after setting all properties.
function sc_CreateFcn(hObject, eventdata, handles)
% hObject    handle to sc (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function maxw_Callback(hObject, eventdata, handles)
% hObject    handle to maxw (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of maxw as text
%        str2double(get(hObject,'String')) returns contents of maxw as a double
guidata(hObject, handles);

% --- Executes during object creation, after setting all properties.
function maxw_CreateFcn(hObject, eventdata, handles)
% hObject    handle to maxw (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on selection change in run.
function run_Callback(hObject, eventdata, handles)
% hObject    handle to run (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns run contents as cell array
%        contents{get(hObject,'Value')} returns selected item from run
guidata(hObject, handles);
% 2 weak prediction
% 3 strong prediction
% 4 two-layer ploting
% 5 RTA by recipe
% 6 RTA by coupling



% --- Executes during object creation, after setting all properties.
function run_CreateFcn(hObject, eventdata, handles)
% hObject    handle to run (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in runb.
function runb_Callback(hObject, eventdata, handles)
% hObject    handle to runb (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
clc;
if get(handles.run,'Value')==1 
    error('Select a Task');
end
handles=control(handles);
guidata(hObject,handles);


function edit17_Callback(hObject, eventdata, handles)
% hObject    handle to edit17 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit17 as text
%        str2double(get(hObject,'String')) returns contents of edit17 as a double


% --- Executes during object creation, after setting all properties.
function edit17_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit17 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit18_Callback(hObject, eventdata, handles)
% hObject    handle to edit18 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit18 as text
%        str2double(get(hObject,'String')) returns contents of edit18 as a double


% --- Executes during object creation, after setting all properties.
function edit18_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit18 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function re_Callback(hObject, eventdata, handles)
% hObject    handle to re (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of re as text
%        str2double(get(hObject,'String')) returns contents of re as a double
temp=str2double(get(hObject,'String'));
set(handles.rtable,'Data',temp);

% --- Executes during object creation, after setting all properties.
function re_CreateFcn(hObject, eventdata, handles)
% hObject    handle to re (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in reb.
function reb_Callback(hObject, eventdata, handles)
% hObject    handle to reb (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
temp = uigetfile('*.txt', 'Select Recipe');
set(handles.re, 'String', temp(1:length(temp)-4));
temp2=importdata(temp);
tempdata=temp2.data;
tempdata=[tempdata; zeros(2,3)];
handles.int=tempdata;
handles.int2=tempdata;
set(handles.rtable,'Data',tempdata);
guidata(hObject, handles);



function minp_Callback(hObject, eventdata, handles)
% hObject    handle to minp (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of minp as text
%        str2double(get(hObject,'String')) returns contents of minp as a double
temp=str2num(get(hObject,'String'));
temp2=str2num(get(handles.minw,'String'));
if temp<temp2
    error('Passband range must be within Wavelength range');
end
guidata(hObject, handles);

% --- Executes during object creation, after setting all properties.
function minp_CreateFcn(hObject, eventdata, handles)
% hObject    handle to minp (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function maxp_Callback(hObject, eventdata, handles)
% hObject    handle to maxp (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of maxp as text
%        str2double(get(hObject,'String')) returns contents of maxp as a double
temp=str2num(get(hObject,'String'));
temp2=str2num(get(handles.maxw,'String'));
if temp>temp2
    error('Passband range must be within Wavelength range');
end
guidata(hObject, handles);

% --- Executes during object creation, after setting all properties.
function maxp_CreateFcn(hObject, eventdata, handles)
% hObject    handle to maxp (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit24_Callback(hObject, eventdata, handles)
% hObject    handle to edit24 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit24 as text
%        str2double(get(hObject,'String')) returns contents of edit24 as a double


% --- Executes during object creation, after setting all properties.
function edit24_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit24 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit25_Callback(hObject, eventdata, handles)
% hObject    handle to edit25 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit25 as text
%        str2double(get(hObject,'String')) returns contents of edit25 as a double


% --- Executes during object creation, after setting all properties.
function edit25_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit25 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit26_Callback(hObject, eventdata, handles)
% hObject    handle to edit26 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit26 as text
%        str2double(get(hObject,'String')) returns contents of edit26 as a double


% --- Executes during object creation, after setting all properties.
function edit26_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit26 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit27_Callback(hObject, eventdata, handles)
% hObject    handle to edit27 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit27 as text
%        str2double(get(hObject,'String')) returns contents of edit27 as a double


% --- Executes during object creation, after setting all properties.
function edit27_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit27 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function w_Callback(hObject, eventdata, handles)
% hObject    handle to w (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of w as text
%        str2double(get(hObject,'String')) returns contents of w as a double
guidata(hObject, handles);

% --- Executes during object creation, after setting all properties.
function w_CreateFcn(hObject, eventdata, handles)
% hObject    handle to w (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function spec_Callback(hObject, eventdata, handles)
% hObject    handle to spec (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of spec as text
%        str2double(get(hObject,'String')) returns contents of spec as a double
guidata(hObject, handles);

% --- Executes during object creation, after setting all properties.
function spec_CreateFcn(hObject, eventdata, handles)
% hObject    handle to spec (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in specb.
function specb_Callback(hObject, eventdata, handles)
% hObject    handle to specb (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
spectra = uigetfile('*.txt', 'Select the txt file for spectra');
set(handles.spec, 'String', spectra(1:length(spectra)-4));
guidata(hObject, handles);



function me_Callback(hObject, eventdata, handles)
% hObject    handle to o3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of o3 as text
%        str2double(get(hObject,'String')) returns contents of o3 as a double


% --- Executes during object creation, after setting all properties.
function me_CreateFcn(hObject, eventdata, handles)
% hObject    handle to o3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function o3_Callback(hObject, eventdata, handles)
% hObject    handle to o3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of o3 as text
%        str2double(get(hObject,'String')) returns contents of o3 as a double


% --- Executes during object creation, after setting all properties.
function o3_CreateFcn(hObject, eventdata, handles)
% hObject    handle to o3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function o2_Callback(hObject, eventdata, handles)
% hObject    handle to o2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of o2 as text
%        str2double(get(hObject,'String')) returns contents of o2 as a double


% --- Executes during object creation, after setting all properties.
function o2_CreateFcn(hObject, eventdata, handles)
% hObject    handle to o2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes when entered data in editable cell(s) in rtable.
function rtable_CellEditCallback(hObject, eventdata, handles)
% hObject    handle to rtable (see GCBO)
% eventdata  structure with the following fields (see MATLAB.UI.CONTROL.TABLE)
%	Indices: row and column indices of the cell(s) edited
%	PreviousData: previous data for the cell(s) edited
%	EditData: string(s) entered by the user
%	NewData: EditData or its converted form set on the Data property. Empty if Data was not changed
%	Error: error string when failed to convert EditData to appropriate value for Data
% handles    structure with handles and user data (see GUIDATA)
temp = get(hObject,'Data');
handles.int=temp;
guidata(hObject,handles)



function o1_Callback(hObject, eventdata, handles)
% hObject    handle to o1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of o1 as text
%        str2double(get(hObject,'String')) returns contents of o1 as a double


% --- Executes during object creation, after setting all properties.
function o1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to o1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function o4_Callback(hObject, eventdata, handles)
% hObject    handle to o4 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of o4 as text
%        str2double(get(hObject,'String')) returns contents of o4 as a double


% --- Executes during object creation, after setting all properties.
function o4_CreateFcn(hObject, eventdata, handles)
% hObject    handle to o4 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function imp_Callback(hObject, eventdata, handles)
% hObject    handle to imp (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of imp as text
%        str2double(get(hObject,'String')) returns contents of imp as a double


% --- Executes during object creation, after setting all properties.
function imp_CreateFcn(hObject, eventdata, handles)
% hObject    handle to imp (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in impb.
function impb_Callback(hObject, eventdata, handles)
% hObject    handle to impb (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
temp = uigetfile('*.txt', 'Select the TEXT (n,k) file for the Impurity');
set(handles.imp, 'String', temp(1:length(temp)-4));
guidata(hObject, handles);



function lr_Callback(hObject, eventdata, handles)
% hObject    handle to lr (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of lr as text
%        str2double(get(hObject,'String')) returns contents of lr as a double


% --- Executes during object creation, after setting all properties.
function lr_CreateFcn(hObject, eventdata, handles)
% hObject    handle to lr (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in lrb.
function lrb_Callback(hObject, eventdata, handles)
% hObject    handle to lrb (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
temp = uigetfile('*.txt', 'Select %R file');
set(handles.lr, 'String',temp);
guidata(hObject, handles);

% --- Executes on button press in lrc.
function lrc_Callback(hObject, eventdata, handles)
% hObject    handle to lrc (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
handles=rmfield(handles,'wavm');
guidata(hObject,handles);


% --- Executes on button press in checkbox1.
function checkbox1_Callback(hObject, eventdata, handles)
% hObject    handle to checkbox1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
guidata(hObject,handles);
% Hint: get(hObject,'Value') returns toggle state of checkbox1


% --- Executes on button press in checkbox2.
function checkbox2_Callback(hObject, eventdata, handles)
% hObject    handle to checkbox2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
guidata(hObject,handles);
% Hint: get(hObject,'Value') returns toggle state of checkbox2


% --- Executes on button press in checkbox3.
function checkbox3_Callback(hObject, eventdata, handles)
% hObject    handle to checkbox3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
guidata(hObject,handles);
% Hint: get(hObject,'Value') returns toggle state of checkbox3


% --- Executes on button press in checkbox4.
function checkbox4_Callback(hObject, eventdata, handles)
% hObject    handle to checkbox4 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
guidata(hObject,handles);
% Hint: get(hObject,'Value') returns toggle state of checkbox4


% --- Executes on slider movement.
function slider2_Callback(hObject, eventdata, handles)
% hObject    handle to slider2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider


% --- Executes during object creation, after setting all properties.
function slider2_CreateFcn(hObject, eventdata, handles)
% hObject    handle to slider2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end



function imp2_Callback(hObject, eventdata, handles)
% hObject    handle to imp2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of imp2 as text
%        str2double(get(hObject,'String')) returns contents of imp2 as a double


% --- Executes during object creation, after setting all properties.
function imp2_CreateFcn(hObject, eventdata, handles)
% hObject    handle to imp2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in imp2b.
function imp2b_Callback(hObject, eventdata, handles)
% hObject    handle to imp2b (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
temp = uigetfile('*.txt', 'Select the TEXT (n,k) file for the Impurity');
set(handles.imp2, 'String', temp(1:length(temp)-4));
guidata(hObject, handles);



function fn_Callback(hObject, eventdata, handles)
% hObject    handle to fn (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of fn as text
%        str2double(get(hObject,'String')) returns contents of fn as a double


% --- Executes during object creation, after setting all properties.
function fn_CreateFcn(hObject, eventdata, handles)
% hObject    handle to fn (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function tf_Callback(hObject, eventdata, handles)
% hObject    handle to tf (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of tf as text
%        str2double(get(hObject,'String')) returns contents of tf as a double


% --- Executes during object creation, after setting all properties.
function tf_CreateFcn(hObject, eventdata, handles)
% hObject    handle to tf (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in tfb.
function tfb_Callback(hObject, eventdata, handles)
% hObject    handle to tfb (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
tf = uigetfile('*.txt', 'Select the Transfer Function file ');
set(handles.tf, 'String', tf(1:length(tf)-4));
guidata(hObject, handles);

% --- Executes on button press in checkbox5.
function checkbox5_Callback(hObject, eventdata, handles)
% hObject    handle to checkbox5 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
guidata(hObject,handles);
% Hint: get(hObject,'Value') returns toggle state of checkbox5


% --- Executes on button press in checkbox6.
function checkbox6_Callback(hObject, eventdata, handles)
% hObject    handle to checkbox6 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of checkbox6



function sen_Callback(hObject, eventdata, handles)
% hObject    handle to sen (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of sen as text
%        str2double(get(hObject,'String')) returns contents of sen as a double
guidata(hObject,handles);

% --- Executes during object creation, after setting all properties.
function sen_CreateFcn(hObject, eventdata, handles)
% hObject    handle to sen (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in checkbox7.
function checkbox7_Callback(hObject, eventdata, handles)
% hObject    handle to checkbox7 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of checkbox7
guidata(hObject,handles);

% --- Executes on button press in checkbox8.
function checkbox8_Callback(hObject, eventdata, handles)
% hObject    handle to checkbox8 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
guidata(hObject,handles);
% Hint: get(hObject,'Value') returns toggle state of checkbox8


% --- Executes on button press in remove.
function remove_Callback(hObject, eventdata, handles)
% hObject    handle to remove (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
[fn,~]=tagcreate(handles);
load('dataset.mat');
Dataset=rmfield(Dataset,fn);
set(handles.ds,'Data',[]);
save('dataset.mat','Dataset');
