function varargout = Nano17_recalibrator2(varargin)
% NANO17_RECALIBRATOR2 MATLAB code for Nano17_recalibrator2.fig
%      NANO17_RECALIBRATOR2, by itself, creates a new NANO17_RECALIBRATOR2 or raises the existing
%      singleton*.
%
%      H = NANO17_RECALIBRATOR2 returns the handle to a new NANO17_RECALIBRATOR2 or the handle to
%      the existing singleton*.
%
%      NANO17_RECALIBRATOR2('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in NANO17_RECALIBRATOR2.M with the given input arguments.
%
%      NANO17_RECALIBRATOR2('Property','Value',...) creates a new NANO17_RECALIBRATOR2 or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before Nano17_recalibrator2_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to Nano17_recalibrator2_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help Nano17_recalibrator2

% Last Modified by GUIDE v2.5 02-Oct-2018 13:22:43

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @Nano17_recalibrator2_OpeningFcn, ...
                   'gui_OutputFcn',  @Nano17_recalibrator2_OutputFcn, ...
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


% --- Executes just before Nano17_recalibrator2 is made visible.
function Nano17_recalibrator2_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to Nano17_recalibrator2 (see VARARGIN)

% Choose default command line output for Nano17_recalibrator2
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes Nano17_recalibrator2 wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = Nano17_recalibrator2_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in pushbutton_opendata.
function pushbutton_opendata_Callback(hObject, eventdata, handles)

[handles.datafilename, handles.pathname]=uigetfile({'*.*'},'pick data file');

if handles.datafilename==0
    return
end

handles.datafile = fullfile(handles.pathname,handles.datafilename);
[blub1,name,handles.extd] = fileparts(handles.datafile);

fid = fopen(handles.datafile);

%handles.M=dlmread(handles.datafile,'\t');
handles.M = importdata(handles.datafile);
handles.M=handles.M';

fclose('all');

set(handles.edit_forcefilename,'String',handles.datafilename);

set(handles.radiobutton_baselined,'value',0);
set(handles.radiobutton_recalibrationdone,'value',0);

cd (handles.pathname);
arrayfun(@cla,findall(0,'type','axes'))

guidata(hObject, handles);
mycalc_retrieverawdata(hObject, eventdata, handles)
% hObject    handle to pushbutton_opendata (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

function mycalc_retrieverawdata(hObject, eventdata, handles)

handles.Fx=handles.M(1:100:end,1);    
handles.Fy=handles.M(1:100:end,2);    
handles.Fz=handles.M(1:100:end,3);    
handles.Tx=handles.M(1:100:end,4);    
handles.Ty=handles.M(1:100:end,5);    
handles.Tz=handles.M(1:100:end,6);  
handles.time=1:length(handles.Fx);

guidata(hObject, handles);
mydisplay1(hObject, eventdata, handles)

function mydisplay1(hObject, eventdata, handles)

axes(handles.axes_originalforces);
     plot(handles.time,handles.Fx,'-r','LineWidth',1,'MarkerEdgeColor','r','MarkerFaceColor','r','MarkerSize',1);
     hold on    
     plot(handles.time,handles.Fy,'-b','LineWidth',1,'MarkerEdgeColor','r','MarkerFaceColor','r','MarkerSize',1);   
     hold on
     plot(handles.time,handles.Fz,'-g','LineWidth',1,'MarkerEdgeColor','r','MarkerFaceColor','r','MarkerSize',1);    
     hold on
     plot(handles.time,0,'-k','LineWidth',1,'MarkerEdgeColor','r','MarkerFaceColor','r','MarkerSize',1);                
     hold off                                                                                                           
     legend('F_x original','F_y original','F_z original','Location','northwest');
    
guidata(hObject, handles);


function pushbutton_baseline_Callback(hObject, eventdata, handles)

%Trim the whole force trace to just the region of interest%
xmin=[];
xmax=[];
xmin1=[];
xmax1=[];

[x,y]=ginput(4);
xmin=round(x(1));
xmin1=xmin(1);
xmax=round(x(2));
xmax1=xmax(1);

xmin=round(x(3));
xmin2=xmin(1);
xmax=round(x(4));
xmax2=xmax(1);

if xmin1<0
    xmin1=1;
end

Fxtrim=handles.Fx(xmin1:xmax2);
Fytrim=handles.Fy(xmin1:xmax2);
Fztrim=handles.Fz(xmin1:xmax2);
Txtrim=handles.Tx(xmin1:xmax2);
Tytrim=handles.Ty(xmin1:xmax2);
Tztrim=handles.Tz(xmin1:xmax2);

% Fxtrim=handles.Fx;
% Fytrim=handles.Fy;
% Fztrim=handles.Fz;
% Txtrim=handles.Tx;
% Tytrim=handles.Ty;
% Tztrim=handles.Tz;
trimtime=1:length(Fxtrim);

%Retrieve .txt file with original calibration matrix coefficients%
OriginalMatrix=dlmread('Nano17_Calib34_Original.txt','\t');

%Convert original forces and torques back to volts%
OriginalForcesTorques=horzcat(Fxtrim,Fytrim,Fztrim,Txtrim,Tytrim,Tztrim);

Volts=(inv(OriginalMatrix)*OriginalForcesTorques')';

V1=Volts(:,1);
V2=Volts(:,2);
V3=Volts(:,3);
V4=Volts(:,4);
V5=Volts(:,5);
V6=Volts(:,6);

%Define baseline for each channel before foot contact%
PrebaselineV1=mean(V1(1:xmax1-xmin1));        
PrebaselineV2=mean(V2(1:xmax1-xmin1));        
PrebaselineV3=mean(V3(1:xmax1-xmin1));        
PrebaselineV5=mean(V5(1:xmax1-xmin1));        
PrebaselineV6=mean(V6(1:xmax1-xmin1));          


%Define baseline for each channel after foot contact
PostbaselineV1=mean(V1(xmin2-xmin1:xmax2-xmin1));       
PostbaselineV2=mean(V2(xmin2-xmin1:xmax2-xmin1));       
PostbaselineV3=mean(V3(xmin2-xmin1:xmax2-xmin1));       
PostbaselineV5=mean(V5(xmin2-xmin1:xmax2-xmin1));       
PostbaselineV6=mean(V6(xmin2-xmin1:xmax2-xmin1));        
    

%Plasticity correction gradient%
mV1=(PrebaselineV1-PostbaselineV1)/(xmax1-xmin2);         
mV2=(PrebaselineV2-PostbaselineV2)/(xmax1-xmin2);        
mV3=(PrebaselineV3-PostbaselineV3)/(xmax1-xmin2);        
mV5=(PrebaselineV5-PostbaselineV5)/(xmax1-xmin2);        
mV6=(PrebaselineV6-PostbaselineV6)/(xmax1-xmin2);           
           
%Reduce signal to baseline and correct for plasticity (if present)%
V1corr=V1-PrebaselineV1-mV1*(trimtime'-(xmax1-xmin1));       
V2corr=V2-PrebaselineV2-mV2*(trimtime'-(xmax1-xmin1));   
V3corr=V3-PrebaselineV3-mV3*(trimtime'-(xmax1-xmin1));   
V5corr=V5-PrebaselineV5-mV5*(trimtime'-(xmax1-xmin1));   
V6corr=V6-PrebaselineV6-mV6*(trimtime'-(xmax1-xmin1));   

%Trim the signal to just that region corresponding to stance%
handles.V1trim=V1corr(xmax1-xmin1:xmin2-xmin1);
handles.V2trim=V2corr(xmax1-xmin1:xmin2-xmin1);
handles.V3trim=V3corr(xmax1-xmin1:xmin2-xmin1);
handles.V5trim=V5corr(xmax1-xmin1:xmin2-xmin1);
handles.V6trim=V6corr(xmax1-xmin1:xmin2-xmin1);

handles.regiontime=1:length(handles.V1trim);

set(handles.radiobutton_baselined,'value',1);
set(handles.radiobutton_recalibrationdone,'value',0);


axes(handles.axes_newforces); 
    plot(trimtime,V1, '-r','LineWidth',1,'MarkerEdgeColor','r','MarkerFaceColor','r','MarkerSize',1);
    hold on 
    plot(trimtime,V2,'-g','LineWidth',1,'MarkerEdgeColor','r','MarkerFaceColor','r','MarkerSize',1);     
    plot(trimtime,V3,'-b','LineWidth',1,'MarkerEdgeColor','r','MarkerFaceColor','r','MarkerSize',1);     
    plot(trimtime,V4,'-k','LineWidth',1,'MarkerEdgeColor','r','MarkerFaceColor','r','MarkerSize',1);     
    plot(trimtime,V5,'-m','LineWidth',1,'MarkerEdgeColor','r','MarkerFaceColor','r','MarkerSize',1);     
    plot(trimtime,V6,'-c','LineWidth',1,'MarkerEdgeColor','r','MarkerFaceColor','r','MarkerSize',1);     
    hold off

guidata(hObject, handles);
% hObject    handle to pushbutton_baseline (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% --- Executes on button press in pushbutton_recalibrate.
function pushbutton_recalibrate_Callback(hObject, eventdata, handles)

V=horzcat(handles.V1trim,handles.V2trim,handles.V3trim,handles.V5trim,handles.V6trim);

%Retrieve .txt files with new calibration matrix coefficients%
C1=dlmread('Calibration_C1.txt','\t');

%Apply new calibration matrix to get new forces and torques%
L=(C1*V')';

Dx=str2double(get(handles.edit_CoPx,'String'));
Dy=str2double(get(handles.edit_CoPy,'String'));

    for i=1:length(handles.regiontime)

    FxCal(i)=L(i,1);
    FyCal(i)=L(i,2);
    FzCal(i)=L(i,3);

    Errorxx=-0.43310*Dy-44.91867;
    Errorxy=0.40563*Dx-27.69494;
    Errorxz=-2.144*Dx-1.388*Dy+1.015;
    Erroryy=0.25120*Dx-17.70618;
    Erroryx=-0.27037*Dy-27.71775;
    Erroryz=-1.339*Dx-0.8617*Dy+0.6609;
    Errorzz=0.05915*Dx+0.03451*Dy-0.4598;
    Errorzx=0.000425*Dx+8.563e-5*Dy+0.01064;
    Errorzy=-7.189e-5*Dx-0.0008874*Dy+0.006654;

    E1=Errorxy/((Erroryy/100)+1);
    E2=Errorxz/((Errorzz/100)+1);
    E3=Erroryx/((Errorxx/100)+1);
    E4=Erroryz/((Errorzz/100)+1);
    E5=Errorzx/((Errorxx/100)+1);
    E6=Errorzy/((Erroryy/100)+1);

    A=[1 E1/100 E2/100; E3/100 1 E4/100; E5/100 E6/100 1];
    K=[FxCal(i); FyCal(i); FzCal(i)];
    U=A\K;

    Xfromx(i)=U(1);
    Yfromy(i)=U(2);
    Zfromz(i)=U(3);

    FxApplied(i)=Xfromx(i)/((Errorxx/100)+1);
    FyApplied(i)=Yfromy(i)/((Erroryy/100)+1);
    FzApplied(i)=Zfromz(i)/((Errorzz/100)+1);

    end

handles.FxRecalib=FxApplied;
handles.FyRecalib=FyApplied;
handles.FzRecalib=FzApplied;

set(handles.radiobutton_recalibrationdone,'value',1);

guidata(hObject, handles);
mydisplay2(hObject, eventdata, handles);
% hObject    handle to pushbutton_recalibrate (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

function mydisplay2(hObject, eventdata, handles)

axes(handles.axes_newforces); 
    plot(handles.regiontime,handles.FxRecalib,'-r','LineWidth',1,'MarkerEdgeColor','r','MarkerFaceColor','r','MarkerSize',1);     
    hold on     
    plot(handles.regiontime,handles.FyRecalib,'-b','LineWidth',1,'MarkerEdgeColor','r','MarkerFaceColor','r','MarkerSize',1);     
    hold on    
    plot(handles.regiontime,handles.FzRecalib,'-g','LineWidth',1,'MarkerEdgeColor','r','MarkerFaceColor','r','MarkerSize',1);     
    hold on    
    plot(handles.regiontime,0,'-k','LineWidth',1,'MarkerEdgeColor','r','MarkerFaceColor','r','MarkerSize',1);
    hold off
    legend('F_x recalibrated','F_y recalibrated','F_z recalibrated','Location','northwest');
    
guidata(hObject, handles);


% --- Executes on button press in pushbutton_save.
function pushbutton_save_Callback(hObject, eventdata, handles)

[pathstr,name,ext]=fileparts(handles.datafilename);

filename=strcat('C:\Users\deathstar\Desktop\gecko forces\',name,'_processed','.txt');

for i=1:length(handles.time),
fid = fopen(filename,'a+');
fprintf(fid, '%6.6f\t %6.6f\t %6.6f\t %6.6f\n',handles.time(i),handles.Fxdata(i),handles.Fydata(i),handles.Fzdata(i));
    fclose(fid);
end

guidata(hObject, handles)
% hObject    handle to pushbutton_save (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)



% --- Executes on button press in pushbutton21.
function pushbutton21_Callback(hObject, eventdata, handles)
[pathstr,name,ext]=fileparts(handles.datafilename);

filename=strcat('C:\Users\deathstar\Desktop\gecko forces\',name,'_processed','.txt');

for i=1:length(handles.regiontime),
fid = fopen(filename,'a+');
fprintf(fid, '%6.6f\t %6.6f\t %6.6f\t %6.6f\n',handles.regiontime(i),handles.FxRecalib(i),handles.FyRecalib(i),handles.FzRecalib(i));
    fclose(fid);
end

guidata(hObject, handles)

function edit_forcefilename_Callback(hObject, eventdata, handles)
% hObject    handle to edit_forcefilename (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_forcefilename as text
%        str2double(get(hObject,'String')) returns contents of edit_forcefilename as a double


% --- Executes during object creation, after setting all properties.
function edit_forcefilename_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_forcefilename (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end




% --- Executes on button press in radiobutton_smoothed.
function radiobutton_smoothed_Callback(hObject, eventdata, handles)
% hObject    handle to radiobutton_smoothed (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobutton_smoothed



function edit_smoothfactorx_Callback(hObject, eventdata, handles)
% hObject    handle to edit_smoothfactorx (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_smoothfactorx as text
%        str2double(get(hObject,'String')) returns contents of edit_smoothfactorx as a double


% --- Executes during object creation, after setting all properties.
function edit_smoothfactorx_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_smoothfactorx (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit_smoothfactory_Callback(hObject, eventdata, handles)
% hObject    handle to edit_smoothfactory (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_smoothfactory as text
%        str2double(get(hObject,'String')) returns contents of edit_smoothfactory as a double


% --- Executes during object creation, after setting all properties.
function edit_smoothfactory_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_smoothfactory (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit_smoothfactorz_Callback(hObject, eventdata, handles)
% hObject    handle to edit_smoothfactorz (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_smoothfactorz as text
%        str2double(get(hObject,'String')) returns contents of edit_smoothfactorz as a double


% --- Executes during object creation, after setting all properties.
function edit_smoothfactorz_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_smoothfactorz (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in radiobutton_settozero.
function radiobutton_settozero_Callback(hObject, eventdata, handles)
% hObject    handle to radiobutton_settozero (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobutton_settozero


% --- Executes on button press in radiobutton_magnifyx.
function radiobutton_magnifyx_Callback(hObject, eventdata, handles)
% hObject    handle to radiobutton_magnifyx (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobutton_magnifyx


% --- Executes on button press in radiobutton_magnifyy.
function radiobutton_magnifyy_Callback(hObject, eventdata, handles)
% hObject    handle to radiobutton_magnifyy (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobutton_magnifyy



function edit_column_Callback(hObject, eventdata, handles)
% hObject    handle to edit_column (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_column as text
%        str2double(get(hObject,'String')) returns contents of edit_column as a double


% --- Executes during object creation, after setting all properties.
function edit_column_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_column (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end




function edit_11_Callback(hObject, eventdata, handles)
% hObject    handle to edit_11 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_11 as text
%        str2double(get(hObject,'String')) returns contents of edit_11 as a double


% --- Executes during object creation, after setting all properties.
function edit_11_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_11 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit_21_Callback(hObject, eventdata, handles)
% hObject    handle to edit_21 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_21 as text
%        str2double(get(hObject,'String')) returns contents of edit_21 as a double


% --- Executes during object creation, after setting all properties.
function edit_21_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_21 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit_31_Callback(hObject, eventdata, handles)
% hObject    handle to edit_31 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_31 as text
%        str2double(get(hObject,'String')) returns contents of edit_31 as a double


% --- Executes during object creation, after setting all properties.
function edit_31_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_31 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit_41_Callback(hObject, eventdata, handles)
% hObject    handle to edit_41 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_41 as text
%        str2double(get(hObject,'String')) returns contents of edit_41 as a double


% --- Executes during object creation, after setting all properties.
function edit_41_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_41 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit_61_Callback(hObject, eventdata, handles)
% hObject    handle to edit_61 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_61 as text
%        str2double(get(hObject,'String')) returns contents of edit_61 as a double


% --- Executes during object creation, after setting all properties.
function edit_61_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_61 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit_51_Callback(hObject, eventdata, handles)
% hObject    handle to edit_51 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_51 as text
%        str2double(get(hObject,'String')) returns contents of edit_51 as a double


% --- Executes during object creation, after setting all properties.
function edit_51_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_51 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit_12_Callback(hObject, eventdata, handles)
% hObject    handle to edit_12 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_12 as text
%        str2double(get(hObject,'String')) returns contents of edit_12 as a double


% --- Executes during object creation, after setting all properties.
function edit_12_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_12 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit_22_Callback(hObject, eventdata, handles)
% hObject    handle to edit_22 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_22 as text
%        str2double(get(hObject,'String')) returns contents of edit_22 as a double


% --- Executes during object creation, after setting all properties.
function edit_22_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_22 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit_32_Callback(hObject, eventdata, handles)
% hObject    handle to edit_32 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_32 as text
%        str2double(get(hObject,'String')) returns contents of edit_32 as a double


% --- Executes during object creation, after setting all properties.
function edit_32_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_32 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit_42_Callback(hObject, eventdata, handles)
% hObject    handle to edit_42 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_42 as text
%        str2double(get(hObject,'String')) returns contents of edit_42 as a double


% --- Executes during object creation, after setting all properties.
function edit_42_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_42 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit_62_Callback(hObject, eventdata, handles)
% hObject    handle to edit_62 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_62 as text
%        str2double(get(hObject,'String')) returns contents of edit_62 as a double


% --- Executes during object creation, after setting all properties.
function edit_62_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_62 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit_52_Callback(hObject, eventdata, handles)
% hObject    handle to edit_52 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_52 as text
%        str2double(get(hObject,'String')) returns contents of edit_52 as a double


% --- Executes during object creation, after setting all properties.
function edit_52_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_52 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit_13_Callback(hObject, eventdata, handles)
% hObject    handle to edit_13 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_13 as text
%        str2double(get(hObject,'String')) returns contents of edit_13 as a double


% --- Executes during object creation, after setting all properties.
function edit_13_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_13 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit_23_Callback(hObject, eventdata, handles)
% hObject    handle to edit_23 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_23 as text
%        str2double(get(hObject,'String')) returns contents of edit_23 as a double


% --- Executes during object creation, after setting all properties.
function edit_23_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_23 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit_33_Callback(hObject, eventdata, handles)
% hObject    handle to edit_33 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_33 as text
%        str2double(get(hObject,'String')) returns contents of edit_33 as a double


% --- Executes during object creation, after setting all properties.
function edit_33_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_33 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit_43_Callback(hObject, eventdata, handles)
% hObject    handle to edit_43 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_43 as text
%        str2double(get(hObject,'String')) returns contents of edit_43 as a double


% --- Executes during object creation, after setting all properties.
function edit_43_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_43 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit_63_Callback(hObject, eventdata, handles)
% hObject    handle to edit_63 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_63 as text
%        str2double(get(hObject,'String')) returns contents of edit_63 as a double


% --- Executes during object creation, after setting all properties.
function edit_63_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_63 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit_53_Callback(hObject, eventdata, handles)
% hObject    handle to edit_53 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_53 as text
%        str2double(get(hObject,'String')) returns contents of edit_53 as a double


% --- Executes during object creation, after setting all properties.
function edit_53_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_53 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit_14_Callback(hObject, eventdata, handles)
% hObject    handle to edit_14 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_14 as text
%        str2double(get(hObject,'String')) returns contents of edit_14 as a double


% --- Executes during object creation, after setting all properties.
function edit_14_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_14 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit_24_Callback(hObject, eventdata, handles)
% hObject    handle to edit_24 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_24 as text
%        str2double(get(hObject,'String')) returns contents of edit_24 as a double


% --- Executes during object creation, after setting all properties.
function edit_24_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_24 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit_34_Callback(hObject, eventdata, handles)
% hObject    handle to edit_34 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_34 as text
%        str2double(get(hObject,'String')) returns contents of edit_34 as a double


% --- Executes during object creation, after setting all properties.
function edit_34_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_34 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit_44_Callback(hObject, eventdata, handles)
% hObject    handle to edit_44 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_44 as text
%        str2double(get(hObject,'String')) returns contents of edit_44 as a double


% --- Executes during object creation, after setting all properties.
function edit_44_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_44 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit_64_Callback(hObject, eventdata, handles)
% hObject    handle to edit_64 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_64 as text
%        str2double(get(hObject,'String')) returns contents of edit_64 as a double


% --- Executes during object creation, after setting all properties.
function edit_64_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_64 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit_54_Callback(hObject, eventdata, handles)
% hObject    handle to edit_54 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_54 as text
%        str2double(get(hObject,'String')) returns contents of edit_54 as a double


% --- Executes during object creation, after setting all properties.
function edit_54_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_54 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit_15_Callback(hObject, eventdata, handles)
% hObject    handle to edit_15 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_15 as text
%        str2double(get(hObject,'String')) returns contents of edit_15 as a double


% --- Executes during object creation, after setting all properties.
function edit_15_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_15 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit_25_Callback(hObject, eventdata, handles)
% hObject    handle to edit_25 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_25 as text
%        str2double(get(hObject,'String')) returns contents of edit_25 as a double


% --- Executes during object creation, after setting all properties.
function edit_25_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_25 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit_35_Callback(hObject, eventdata, handles)
% hObject    handle to edit_35 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_35 as text
%        str2double(get(hObject,'String')) returns contents of edit_35 as a double


% --- Executes during object creation, after setting all properties.
function edit_35_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_35 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit_45_Callback(hObject, eventdata, handles)
% hObject    handle to edit_45 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_45 as text
%        str2double(get(hObject,'String')) returns contents of edit_45 as a double


% --- Executes during object creation, after setting all properties.
function edit_45_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_45 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit_65_Callback(hObject, eventdata, handles)
% hObject    handle to edit_65 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_65 as text
%        str2double(get(hObject,'String')) returns contents of edit_65 as a double


% --- Executes during object creation, after setting all properties.
function edit_65_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_65 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit_55_Callback(hObject, eventdata, handles)
% hObject    handle to edit_55 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_55 as text
%        str2double(get(hObject,'String')) returns contents of edit_55 as a double


% --- Executes during object creation, after setting all properties.
function edit_55_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_55 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit_16_Callback(hObject, eventdata, handles)
% hObject    handle to edit_16 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_16 as text
%        str2double(get(hObject,'String')) returns contents of edit_16 as a double


% --- Executes during object creation, after setting all properties.
function edit_16_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_16 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit_26_Callback(hObject, eventdata, handles)
% hObject    handle to edit_26 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_26 as text
%        str2double(get(hObject,'String')) returns contents of edit_26 as a double


% --- Executes during object creation, after setting all properties.
function edit_26_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_26 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit_36_Callback(hObject, eventdata, handles)
% hObject    handle to edit_36 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_36 as text
%        str2double(get(hObject,'String')) returns contents of edit_36 as a double


% --- Executes during object creation, after setting all properties.
function edit_36_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_36 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit_46_Callback(hObject, eventdata, handles)
% hObject    handle to edit_46 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_46 as text
%        str2double(get(hObject,'String')) returns contents of edit_46 as a double


% --- Executes during object creation, after setting all properties.
function edit_46_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_46 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit_66_Callback(hObject, eventdata, handles)
% hObject    handle to edit_66 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_66 as text
%        str2double(get(hObject,'String')) returns contents of edit_66 as a double


% --- Executes during object creation, after setting all properties.
function edit_66_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_66 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit_56_Callback(hObject, eventdata, handles)
% hObject    handle to edit_56 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_56 as text
%        str2double(get(hObject,'String')) returns contents of edit_56 as a double


% --- Executes during object creation, after setting all properties.
function edit_56_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_56 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in radiobutton_recalibrationdone.
function radiobutton_recalibrationdone_Callback(hObject, eventdata, handles)
% hObject    handle to radiobutton_recalibrationdone (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobutton_recalibrationdone


% --- Executes on button press in radiobutton_baselined.
function radiobutton_baselined_Callback(hObject, eventdata, handles)
% hObject    handle to radiobutton_baselined (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobutton_baselined



function edit_CoPx_Callback(hObject, eventdata, handles)
% hObject    handle to edit_CoPx (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_CoPx as text
%        str2double(get(hObject,'String')) returns contents of edit_CoPx as a double


% --- Executes during object creation, after setting all properties.
function edit_CoPx_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_CoPx (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit_CoPy_Callback(hObject, eventdata, handles)
% hObject    handle to edit_CoPy (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_CoPy as text
%        str2double(get(hObject,'String')) returns contents of edit_CoPy as a double


% --- Executes during object creation, after setting all properties.
function edit_CoPy_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_CoPy (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in radiobutton_trimmed.
function radiobutton_trimmed_Callback(hObject, eventdata, handles)
% hObject    handle to radiobutton_trimmed (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobutton_trimmed
