function varargout = Gecko_forces_sync(varargin)
% GECKO_FORCES_SYNC MATLAB code for Gecko_forces_sync.fig
%      GECKO_FORCES_SYNC, by itself, creates a new GECKO_FORCES_SYNC or raises the existing
%      singleton*.
%
%      H = GECKO_FORCES_SYNC returns the handle to a new GECKO_FORCES_SYNC or the handle to
%      the existing singleton*.
%
%      GECKO_FORCES_SYNC('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in GECKO_FORCES_SYNC.M with the given input arguments.
%
%      GECKO_FORCES_SYNC('Property','Value',...) creates a new GECKO_FORCES_SYNC or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before Gecko_forces_sync_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to Gecko_forces_sync_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help Gecko_forces_sync

% Last Modified by GUIDE v2.5 07-Oct-2018 19:24:19

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @Gecko_forces_sync_OpeningFcn, ...
                   'gui_OutputFcn',  @Gecko_forces_sync_OutputFcn, ...
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


function pathname_Callback(hObject, eventdata, handles)
% hObject    handle to pathname (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

try
    handles.str = get(handles.figure1,'UserData');
    
    [selection,selected] = listdlg('PromptString','Select a path:','SelectionMode','single','ListSize',[300 300],...
                    'ListString',handles.str);
    switch selection
        case 1  %add new path
            [~, handles.pathname]=uigetfile('*.*','select folder'); 
            handles.str{end+1}=handles.pathname;
            cd(handles.pathname);
            set(handles.figure1,'UserData',handles.str);
        case 3  %delete path
            [selection,selected] = listdlg('PromptString','Select path to be deleted','SelectionMode','single','ListSize',[300 300],...
                    'ListString',handles.str);
            handles.str(selection)=[];
            set(handles.figure1,'UserData',handles.str);
        otherwise
            handles.pathname=handles.str{selection};
            cd(handles.pathname);
    end
    guidata(hObject, handles);
catch
    if ~isfield(handles,'pathname')
        h = errordlg('You have not selected any path!','Error');        
    end
end


% --- Executes just before Gecko_forces_sync is made visible.
function Gecko_forces_sync_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to Gecko_forces_sync (see VARARGIN)

% Choose default command line output for Gecko_forces_sync
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes Gecko_forces_sync wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = Gecko_forces_sync_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;

%plots the video
function mydisplay(hObject, eventdata, handles)

% open and show video frame
axes(handles.axes1);
if ~isempty(handles.videofile) 
    if strcmp(handles.ext,'.avi') || strcmp(handles.ext,'.AVI')|| strcmp(handles.ext,'.MP4') || strcmp(handles.ext,'.MPG') || strcmp(handles.ext,'.MOV')
            mov = read(handles.video, handles.frame);
            
    elseif strcmp(handles.ext,'.seq')
        [mov, ~, handles.totalframes] = readsinglestreampix(handles.videofile,handles.frame);
    elseif  strcmp(handles.ext,'.tif')|| strcmp(handles.ext,'.jpg') || strcmp(handles.ext,'.bmp')
        mov =imread(handles.videofile);
    end
    imshow(mov);
end

          if get(handles.radiobutton4, 'value') ==1
                           %top=1
                            axes(handles.axes1);
                            
                           varY=handles.FyRecalib_smoothed(handles.frame*handles.Cfact);
                           varX=handles.FxRecalib_smoothed(handles.frame*handles.Cfact);
                           line([handles.xpos-varY*4000,handles.xpos],[handles.ypos+varX*4000,handles.ypos],'LineWidth',1,'Color','r')
          end  

guidata(hObject, handles);

function mydisplay2(hObject, eventdata, handles)

axes(handles.axes2); 
    plot(handles.regiontime,handles.FxRecalib,'-r','LineWidth',1,'MarkerEdgeColor','r','MarkerFaceColor','r','MarkerSize',1);     
    hold on     
    plot(handles.regiontime,handles.FyRecalib,'-b','LineWidth',1,'MarkerEdgeColor','r','MarkerFaceColor','r','MarkerSize',1);     
    hold on    
    plot(handles.regiontime,handles.FzRecalib,'-g','LineWidth',1,'MarkerEdgeColor','r','MarkerFaceColor','r','MarkerSize',1);     
    hold on    
    plot(handles.regiontime,0,'-k','LineWidth',1,'MarkerEdgeColor','r','MarkerFaceColor','r','MarkerSize',1);
    hold off
    vline(handles.frame*handles.Cfact)  
    legend('F_x recalibrated','F_y recalibrated','F_z recalibrated','Location','northeast');
    
guidata(hObject, handles);

function mydisplay3(hObject, eventdata, handles)


    
guidata(hObject, handles);

function mydisp(hObject, eventdata, handles)

    if get(handles.radiobutton2_cali,'Value')
        
        if get(handles.radiobutton3,'Value')
        
        %displays the corrected and smoothed data    
        axes(handles.axes2);
        plot(handles.regiontime,handles.FxRecalib_smoothed,'-r','LineWidth',1,'MarkerEdgeColor','r','MarkerFaceColor','r','MarkerSize',1);     
        hold on     
        plot(handles.regiontime,handles.FyRecalib_smoothed,'-b','LineWidth',1,'MarkerEdgeColor','r','MarkerFaceColor','r','MarkerSize',1);     
        plot(handles.regiontime,handles.FzRecalib_smoothed,'-g','LineWidth',1,'MarkerEdgeColor','r','MarkerFaceColor','r','MarkerSize',1);     
        hold off    
        vline(handles.frame*handles.Cfact)  
        legend('F_x recalibrated','F_y recalibrated','F_z recalibrated','Location','northeast');
        
        else
        
        %display data corrected for Nano17 error    
        axes(handles.axes2);
        plot(handles.regiontime,handles.FxRecalib,'-r','LineWidth',1,'MarkerEdgeColor','r','MarkerFaceColor','r','MarkerSize',1);     
        hold on     
        plot(handles.regiontime,handles.FyRecalib,'-b','LineWidth',1,'MarkerEdgeColor','r','MarkerFaceColor','r','MarkerSize',1);     
        plot(handles.regiontime,handles.FzRecalib,'-g','LineWidth',1,'MarkerEdgeColor','r','MarkerFaceColor','r','MarkerSize',1);     
        hold off    
        vline(handles.frame*handles.Cfact)  
        legend('F_x recalibrated','F_y recalibrated','F_z recalibrated','Location','northeast');    
            
        end
            
        
        
    else
        
        %Raw force data
        axes(handles.axes2);
        plot(handles.time,handles.Fx,'-r','LineWidth',1,'MarkerEdgeColor','r','MarkerFaceColor','r','MarkerSize',1);
        hold on
        plot(handles.time,handles.Fy,'-b','LineWidth',1,'MarkerEdgeColor','b','MarkerFaceColor','b','MarkerSize',1);
        plot(handles.time,handles.Fz,'-g','LineWidth',1,'MarkerEdgeColor','g','MarkerFaceColor','g','MarkerSize',1);
        hold off
        vline(handles.frame*handles.Cfact)  
        
    end
        
guidata(hObject, handles);

function mycalc(hObject, eventdata, handles)

totf=str2double(get(handles.edit2_totalframes, 'String'));

trigger=round(str2double(get(handles.edit3_trigger, 'String')));
% tno=str2double(get(handles.edit12_TFN, 'String'));
% trigger=9254;

framerate=str2double(get(handles.edit5_fr, 'String'));
samplingF=str2double(get(handles.edit6_sf, 'String'));
handles.Cfact=samplingF/framerate;

handles.Fx=handles.M((trigger-(totf*handles.Cfact)):trigger,1);
handles.Fy=handles.M((trigger-(totf*handles.Cfact)):trigger,2);
handles.Fz=handles.M((trigger-(totf*handles.Cfact)):trigger,3);
handles.Tx=handles.M((trigger-(totf*handles.Cfact)):trigger,4);
handles.Ty=handles.M((trigger-(totf*handles.Cfact)):trigger,5);
handles.Tz=handles.M((trigger-(totf*handles.Cfact)):trigger,6);
handles.time=1:length(handles.Fx);



% handles.X=handles.M(:,2);
% handles.Y=handles.M(:,3);
% handles.Z=handles.M(:,4);
% handles.time=1:length(handles.Z);

guidata(hObject, handles);
mydisp(hObject, eventdata, handles)









%%%%%%%%%%%%%%%%%%          Buttons


% STEP 1:
% --- Executes on button press in pushbutton1_video.
function pushbutton1_video_Callback(hObject, eventdata, handles)
[handles.videofilename, handles.pathname]=uigetfile({'*.MOV;*.avi;*.MP4;*.seq','Video files';'*.tif;*.jpg;*.bmp', 'Image files'},'pick file');
handles.videofile = fullfile(handles.pathname,handles.videofilename);
[~,handles.name,handles.ext] = fileparts(handles.videofile);

 cd (handles.pathname);

% avi files, initialise
    if strcmp(handles.ext,'.avi') || strcmp(handles.ext,'.AVI')|| strcmp(handles.ext,'.MP4') || strcmp(handles.ext,'.MPG')
        video = VideoReader(handles.videofile);
        handles.video=video;
        handles.totalframes = video.NumberOfFrames;
        handles.height = video.Height;
        handles.width = video.Width;
        handles.white= 2^(video.BitsPerPixel/3)-1; %maximum greyscale value, normally 255
%         set(handles.threshold,'max',handles.white);
%         set(handles.threshold,'Value',str2double(get(handles.edit_threshold,'String')));
        handles.framerate = video.FrameRate;
        
          elseif strcmp(handles.ext,'.MOV')
        video = VideoReader(handles.videofile);
        handles.video=video;
        handles.totalframes = video.NumberOfFrames;
        handles.height = video.Height;
        handles.width = video.Width;
        handles.white= 2^(video.BitsPerPixel/3)-1; 
        handles.framerate = video.FrameRate;
    end
    
set(handles.slider1,'max',handles.totalframes, 'min',1,'Value',1);
set(handles.edit1_filename,'String',handles.videofilename);
set(handles.edit2_totalframes,'String',num2str(handles.totalframes));

set(handles.radiobutton3,'Value',0)
set(handles.radiobutton4,'Value',0)
set(handles.radiobutton2_cali,'Value',0)
set(handles.radiobutton1_bl,'Value',0)

handles.frame=1;
%handles.rect=[];

arrayfun(@cla,findall(0,'type','axes'))

guidata(hObject, handles);
mydisplay(hObject, eventdata, handles)


% ------------------------------------------------------------------------
% STEP 2:
% --- Executes on button press in pushbutton2_force.
% Opens the explorer, so user can select the force file belonging to
% selected video
function pushbutton2_force_Callback(hObject, eventdata, handles)
[handles.datafilename, handles.pathname]=uigetfile({'*.*'},'pick data file');

if handles.datafilename==0
    return
end

handles.datafile = fullfile(handles.pathname,handles.datafilename);
[blub1,name,handles.extd] = fileparts(handles.datafile);

fid = fopen(handles.datafile);

handles.M=importdata(handles.datafile,'\t');
handles.M=handles.M';

guidata(hObject, handles);
mycalc(hObject, eventdata, handles)



% --- Executes on button press in pushbutton3_points.
function pushbutton3_points_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton3_points (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% --- Executes on button press in pushbutton4_forward.
function pushbutton4_forward_Callback(hObject, eventdata, handles)

%step=str2double(get(handles.edit1_step, 'String'));
step=1;

for i=handles.frame+1:step:handles.totalframes
    handles.frame=i;
    guidata(hObject,handles);
    set(handles.slider1,'Value',handles.frame);
    set(handles.edit4_frame,'String',num2str(handles.frame));
    mydisplay(hObject, eventdata, handles);
    mydisp(hObject, eventdata, handles);
        
    if get(handles.Stop,'Value')
        set(handles.Stop,'Value',0)
        break
    end
end


% ------------------------------------------------------------------------
% STEP 3:
% --- Executes on button press in pushbutton6_bl. -> baseline
function pushbutton6_bl_Callback(hObject, eventdata, handles)


% %Retrieve .txt file with original calibration matrix coefficients%
% OriginalMatrix=dlmread('Nano17_Calib34_Original.txt','\t');
% 
% Fxtrim=handles.Fx;
% Fytrim=handles.Fy;
% Fztrim=handles.Fz;
% Txtrim=handles.Tx;
% Tytrim=handles.Ty;
% Tztrim=handles.Tz;
% trimtime=1:length(Fxtrim);
% 
% %Convert original forces and torques back to volts%
% OriginalForcesTorques=horzcat(Fxtrim,Fytrim,Fztrim,Txtrim,Tytrim,Tztrim);
% 
% Volts=(inv(OriginalMatrix)*OriginalForcesTorques')';
% Volts=(inv(OriginalMatrix)*OriginalForcesTorques')';
% 
% V1=Volts(:,1);
% V2=Volts(:,2);
% V3=Volts(:,3);
% V4=Volts(:,4);
% V5=Volts(:,5);
% V6=Volts(:,6);
% 
% axes(handles.axes2); 
%     plot(trimtime,V1,'-r','LineWidth',1,'MarkerEdgeColor','r','MarkerFaceColor','r','MarkerSize',1);     
%     hold on     
%     plot(trimtime,V2,'-b','LineWidth',1,'MarkerEdgeColor','r','MarkerFaceColor','r','MarkerSize',1);     
%     hold on    
%     plot(trimtime,V3,'-g','LineWidth',1,'MarkerEdgeColor','r','MarkerFaceColor','r','MarkerSize',1);     
%     hold on    
%     plot(trimtime,V4,'-k','LineWidth',1,'MarkerEdgeColor','r','MarkerFaceColor','r','MarkerSize',1);
%     hold on    
%     plot(trimtime,V5,'-m','LineWidth',1,'MarkerEdgeColor','r','MarkerFaceColor','r','MarkerSize',1);
%     hold on    
%     plot(trimtime,V6,'-y','LineWidth',1,'MarkerEdgeColor','r','MarkerFaceColor','r','MarkerSize',1);
%     hold off
%     legend('V1','V2','V3','V4','V5','V6','Location','northwest');


%define the baseline before and after

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

%Retrieve .txt file with original calibration matrix coefficients%
OriginalMatrix=dlmread('Nano17_Calib34_Original.txt','\t');

OriginalForcesTorques=horzcat(handles.Fx,handles.Fy,handles.Fz,handles.Tx,handles.Ty,handles.Tz);
trimtime=1:length(handles.Fx);

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

%Dont Trim the signal to just that region corresponding to stance%
%this code just here to keep variable names consistent
handles.V1trim=V1corr;
handles.V2trim=V2corr;
handles.V3trim=V3corr;
handles.V5trim=V5corr;
handles.V6trim=V6corr;

handles.regiontime=1:length(handles.V1trim);

set(handles.radiobutton1_bl,'value',1);
set(handles.radiobutton2_cali,'value',0);

axes(handles.axes2); 
    plot(handles.regiontime,V1, '-r','LineWidth',1,'MarkerEdgeColor','r','MarkerFaceColor','r','MarkerSize',1);
    hold on 
    plot(handles.regiontime,V2,'-g','LineWidth',1,'MarkerEdgeColor','r','MarkerFaceColor','r','MarkerSize',1);     
    plot(handles.regiontime,V3,'-b','LineWidth',1,'MarkerEdgeColor','r','MarkerFaceColor','r','MarkerSize',1);     
    plot(handles.regiontime,V4,'-y','LineWidth',1,'MarkerEdgeColor','r','MarkerFaceColor','r','MarkerSize',1);     
    plot(handles.regiontime,V5,'-m','LineWidth',1,'MarkerEdgeColor','r','MarkerFaceColor','r','MarkerSize',1);     
    plot(handles.regiontime,V6,'-c','LineWidth',1,'MarkerEdgeColor','r','MarkerFaceColor','r','MarkerSize',1);     
    hold off
    

guidata(hObject, handles);


% --- Executes on button press in pushbutton7_recali.
% This is currently executed as step3 hence before the CoP is selected.
% Does is just take CoP = 0,0 as default for this calculation?
function pushbutton7_recali_Callback(hObject, eventdata, handles)

V=horzcat(handles.V1trim,handles.V2trim,handles.V3trim,handles.V5trim,handles.V6trim);

%Retrieve .txt files with new calibration matrix coefficients%
C1=dlmread('Calibration_C1.txt','\t');

%Apply new calibration matrix to get new forces and torques%
L=(C1*V')';

Dx=str2double(get(handles.edit7,'String'));
Dy=str2double(get(handles.edit8,'String'));

for i=1:length(handles.regiontime),

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

set(handles.radiobutton2_cali,'value',1);

guidata(hObject, handles);
mydisplay2(hObject, eventdata, handles);



% ------------------------------------------------------------------------
% STEP 4:
% --- Executes on button press in pushbutton8_smooth.
% Takes the user input for the different smoothing values x,y,z and plots
% the smoothed force data
function pushbutton8_smooth_Callback(hObject, eventdata, handles)

smoothfactx=str2double(get(handles.edit9_smooth, 'String'));
smoothfacty=str2double(get(handles.edit11, 'String'));
smoothfactz=str2double(get(handles.edit12, 'String'));

time2=1:length(handles.Fx);
[spX,valuesZ] = spaps(time2,handles.FxRecalib,smoothfactx);
handles.FxRecalib_smoothed=valuesZ';

[spX,valuesZ] = spaps(time2,handles.FyRecalib,smoothfacty);
handles.FyRecalib_smoothed=valuesZ';

[spX,valuesZ] = spaps(time2,handles.FzRecalib,smoothfactz);
handles.FzRecalib_smoothed=valuesZ';

time1=1:length(handles.FxRecalib_smoothed);

axes(handles.axes2);
plot(time2,handles.FxRecalib,'.r')
hold on
plot(time2,handles.FyRecalib,'.b')
plot(time2,handles.FzRecalib,'.g')
plot(time1,handles.FxRecalib_smoothed,'-b')
plot(time1,handles.FyRecalib_smoothed,'-r')
plot(time1,handles.FzRecalib_smoothed,'-b')
hold off

guidata(hObject, handles);


% ------------------------------------------------------------------------
% STEP 5:
% --- Executes on button press in pushbutton9_range.
% User is asked to select the range of the footfall in the plot,
% min, max, mean and integral values for this range are computed.
function pushbutton9_range_Callback(hObject, eventdata, handles)


xmin=[];
xmax=[];
xmin1=[];
xmax1=[];

[x,y]=ginput(2);

xmin=round(x(1));
xmin1=xmin(1);
xmax=round(x(2));
xmax1=xmax(1);

Fxtrim=handles.FxRecalib_smoothed(xmin1:xmax1);
Fytrim=handles.FyRecalib_smoothed(xmin1:xmax1);
Fztrim=handles.FzRecalib_smoothed(xmin1:xmax1);

%set edit boxes 13 - 15 to mean values
set(handles.edit13,'string',num2str(mean(Fxtrim)));
set(handles.edit14,'string',num2str(mean(Fytrim)));
set(handles.edit15,'string',num2str(mean(Fztrim)));

%set edit boxes 22 - 24 to min values
set(handles.edit22,'string',num2str(min(Fxtrim)));
set(handles.edit23,'string',num2str(min(Fytrim)));
set(handles.edit24,'string',num2str(min(Fztrim)));

%set edit boxes 25 - 27 to max values
set(handles.edit25,'string',num2str(max(Fxtrim)));
set(handles.edit26,'string',num2str(max(Fytrim)));
set(handles.edit27,'string',num2str(max(Fztrim)));

%set edit boxes 19 - 21 to intregral values
samplingF=10000;
set(handles.edit19,'string',num2str(trapz(Fxtrim)/samplingF));
set(handles.edit20,'string',num2str(trapz(Fytrim)/samplingF));
set(handles.edit21,'string',num2str(trapz(Fztrim)/samplingF));

guidata(hObject, handles);


% --- Executes on button press in pushbutton10_origin.
% The user is asked to click on the foot when it's on the forceplate to
% define the CoP of the footfall.
function pushbutton10_origin_Callback(hObject, eventdata, handles)

[x,y]=ginput(1);
handles.xpos=round(x(1));
handles.ypos=round(y(1));

set(handles.radiobutton4,'Value',1)

guidata(hObject, handles);
mydisplay(hObject, eventdata, handles);



% ------------------------------------------------------------------------
% STEP 6:
% --- Executes on button press in pushbutton11_save.
% saves the mean, max, min, and integral as well as the corrected raw force
% data
function pushbutton11_save_Callback(hObject, eventdata, handles)

[pathstr,name,ext]=fileparts(handles.datafilename);

filename=strcat('D:\Jojo\PhD\ClimbingRobot\ClimbingLizardForceAnalysis\forceData_hfren\correctedForces\',name,'_processed','.txt');

for i=1:length(handles.time),
    fid = fopen(filename,'a+');
    fprintf(fid, '%6.6f\t %6.6f\t %6.6f\t %6.6f\n',handles.time(i),handles.FxRecalib(i),handles.FyRecalib(i),handles.FzRecalib(i));
    fclose(fid);
end

h1='filename';
h2='MeanX';
h3='MeanY';
h4='MeanZ';
h5='IntergralX';
h6='IntergralY';
h7='IntergralZ';
h8='MinX';
h9='MinY';
h10='MinZ';
h11='MaxX';
h12='MaxY';
h13='MaxZ';

v1=get(handles.edit1_filename,'String');%filename
v2=str2double(get(handles.edit13,'String'));     %mean x
v3=str2double(get(handles.edit14,'String'));     %mean y
v4=str2double(get(handles.edit15,'String'));     %mean z
v5=str2double(get(handles.edit19,'String'));     %int x
v6=str2double(get(handles.edit20,'String'));     %int x
v7=str2double(get(handles.edit21,'String'));     %int x
v8=str2double(get(handles.edit22,'String'));     %min x
v9=str2double(get(handles.edit23,'String'));     %min x
v10=str2double(get(handles.edit24,'String'));    %min x
v11=str2double(get(handles.edit25,'String'));    %max x
v12=str2double(get(handles.edit26,'String'));    %max y
v13=str2double(get(handles.edit27,'String'));    %max z


path='D:\Jojo\PhD\ClimbingRobot\ClimbingLizardForceAnalysis\forceData_hfren\correctedForces\';
name='Gecko_forces_sync_output.txt';
filename=strcat(path,name);

%change this code to correct path 
fid = fopen(filename,'a+');
if (get(handles.radiobutton13,'Value'))==1
       fprintf(fid,'%s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\n %s\t %6.6f\t %6.6f\t %6.6f\t %6.6f\t %6.6f\t %6.6f\t %6.6f\t %6.6f\t %6.6f\t %6.6f\t %6.6f\t %6.6f\n',h1,h2,h3,h4,h5,h6,h7,h8,h9,h10,h11,h12,h13,v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12,v13);
else    
       fprintf(fid,'%s\t %6.6f\t %6.6f\t %6.6f\t %6.6f\t %6.6f\t %6.6f\t %6.6f\t %6.6f\t %6.6f\t %6.6f\t %6.6f\t %6.6f\n',v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12,v13);
end
fclose(fid);

% %save png file of the figure
% ax = gca;
% ax.Units = 'pixels';
% pos = ax.Position;
% marg = 30;
% rect = [-marg, -marg, pos(3)+1*marg+2, pos(4)+1*marg+1];
% img = getframe(handles.axes1, rect);
% imwrite(img.cdata, [Path, v1, '.jpg']);


guidata(hObject, handles)


% hObject    handle to pushbutton11_save (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)











%%%%%%%%%%%%%%%radio buttons

% --- Executes on button press in radiobutton1_bl.
function radiobutton1_bl_Callback(hObject, eventdata, handles)
% hObject    handle to radiobutton1_bl (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --- Executes on button press in radiobutton2_cali.
function radiobutton2_cali_Callback(hObject, eventdata, handles)
% hObject    handle to radiobutton2_cali (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --- Executes on button press in radiobutton3.
function radiobutton3_Callback(hObject, eventdata, handles)
mydisp(hObject, eventdata, handles)


% --- Executes on button press in radiobutton4.
function radiobutton4_Callback(hObject, eventdata, handles)


% --- Executes on button press in radiobutton5_hind.
function radiobutton5_hind_Callback(hObject, eventdata, handles)
set(handles.radiobutton6_fore,'Value',0)


% --- Executes on button press in radiobutton6_fore.
function radiobutton6_fore_Callback(hObject, eventdata, handles)
set(handles.radiobutton5_hind,'Value',0)


% --- Executes on button press in radiobutton7_up.
function radiobutton7_up_Callback(hObject, eventdata, handles)
set(handles.radiobutton8_down,'Value',0)


% --- Executes on button press in radiobutton8_down.
function radiobutton8_down_Callback(hObject, eventdata, handles)
set(handles.radiobutton7_up,'Value',0)


% --- Executes on button press in radiobutton13.
function radiobutton13_Callback(hObject, eventdata, handles)









%%%%%%%%%%%%%%%%%%          SLIDERS


% --- Executes on slider movement.
function slider1_Callback(hObject, eventdata, handles)
handles.frame=round(get(handles.slider1,'Value'));

if handles.frame>handles.totalframes
    handles.frame=handles.totalframes;
elseif handles.frame<1
    handles.frame=1;
end

set(handles.slider1,'Value',handles.frame);
set(handles.edit4_frame,'String',num2str(handles.frame));


guidata(hObject,handles);
mydisplay(hObject, eventdata, handles)
mydisp(hObject, eventdata, handles);


% --- Executes during object creation, after setting all properties.
function slider1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to slider1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end












%%%%%%%%%%%%%%%%%          EDIT boxes


% --- Executes on button press in Stop.
function Stop_Callback(hObject, eventdata, handles)
% hObject    handle to Stop (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

function edit1_filename_Callback(hObject, eventdata, handles)
% hObject    handle to edit1_filename (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% --- Executes during object creation, after setting all properties.
function edit1_filename_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit1_filename (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

function edit2_totalframes_Callback(hObject, eventdata, handles)
% hObject    handle to edit2_totalframes (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% --- Executes during object creation, after setting all properties.
function edit2_totalframes_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit2_totalframes (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

function edit3_trigger_Callback(hObject, eventdata, handles)
% hObject    handle to edit3_trigger (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% --- Executes during object creation, after setting all properties.
function edit3_trigger_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit3_trigger (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

function edit4_frame_Callback(hObject, eventdata, handles)
% hObject    handle to edit4_frame (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% --- Executes during object creation, after setting all properties.
function edit4_frame_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit4_frame (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

function edit5_fr_Callback(hObject, eventdata, handles)
% hObject    handle to edit5_fr (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% --- Executes during object creation, after setting all properties.
function edit5_fr_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit5_fr (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

function edit6_sf_Callback(hObject, eventdata, handles)
% hObject    handle to edit6_sf (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% --- Executes during object creation, after setting all properties.
function edit6_sf_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit6_sf (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


function edit7_Callback(hObject, eventdata, handles)
% hObject    handle to edit7 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% --- Executes during object creation, after setting all properties.
function edit7_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit7 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

function edit8_Callback(hObject, eventdata, handles)
% hObject    handle to edit8 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

function edit8_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit8 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

function edit9_smooth_Callback(hObject, eventdata, handles)
% hObject    handle to edit9_smooth (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

function edit9_smooth_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit9_smooth (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


function edit11_Callback(hObject, eventdata, handles)
% hObject    handle to edit11 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --- Executes during object creation, after setting all properties.
function edit11_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit11 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


function edit12_Callback(hObject, eventdata, handles)
% hObject    handle to edit12 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% --- Executes during object creation, after setting all properties.
function edit12_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit12 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



%13-15 x,y,z means

function edit13_Callback(hObject, eventdata, handles)
% hObject    handle to edit13 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --- Executes during object creation, after setting all properties.
function edit13_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit13 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


function edit14_Callback(hObject, eventdata, handles)
% hObject    handle to edit14 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --- Executes during object creation, after setting all properties.
function edit14_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit14 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


function edit15_Callback(hObject, eventdata, handles)
% hObject    handle to edit15 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --- Executes during object creation, after setting all properties.
function edit15_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit15 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



%19-21 x,y,z integrals

function edit19_Callback(hObject, eventdata, handles)
% hObject    handle to edit19 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --- Executes during object creation, after setting all properties.
function edit19_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit19 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


function edit20_Callback(hObject, eventdata, handles)
% hObject    handle to edit20 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --- Executes during object creation, after setting all properties.
function edit20_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit20 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


function edit21_Callback(hObject, eventdata, handles)
% hObject    handle to edit21 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)



% --- Executes during object creation, after setting all properties.
function edit21_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit21 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit22_Callback(hObject, eventdata, handles)
% hObject    handle to edit22 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --- Executes during object creation, after setting all properties.
function edit22_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit22 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit23_Callback(hObject, eventdata, handles)
% hObject    handle to edit23 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --- Executes during object creation, after setting all properties.
function edit23_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit23 (see GCBO)
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
