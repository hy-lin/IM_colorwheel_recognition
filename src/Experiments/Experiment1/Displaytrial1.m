function trial = Displaytrial1(visualInfo, expInfo, trial, autoPilot)

t = GetSecs;
maxrect=SCREEN(visualInfo.mainPtr,'Rect');
maxx = maxrect(3); maxy = maxrect(4);
X = maxx/2; Y = maxy/2;
SCREEN(visualInfo.mainPtr,'FillRect');
rectangle = [trial.coordx'-visualInfo.frameWidth/2, trial.coordy'-visualInfo.frameHeight/2, trial.coordx'+visualInfo.frameWidth/2, trial.coordy'+visualInfo.frameHeight/2];

%prepare the response

% draw colorwheel (in debug mode only)
if expInfo.debug,
	SCREEN(visualInfo.colorwheelPtr,'FillRect');
	shift = DisplayColorWheel(visualInfo, visualInfo.colorwheelPtr, trial);
	SCREEN('CopyWindow', visualInfo.colorwheelPtr, visualInfo.targetPtr);
end;

for square = 1:trial.setsize
	SCREEN(visualInfo.targetPtr,'FrameRect', visualInfo.fgColor, rectangle(square,:),visualInfo.penWidth,visualInfo.penWidth);  %thin frames around other objects
end
	
SCREEN(visualInfo.targetPtr,'FillRect', trial.probeColor, rectangle(1,:)); % draw the probe, I have to make sure that there will be no frame around it. 

% prepare stimuli
SCREEN(visualInfo.stimulusPtr,'FillRect');    %wipe background stimuli window
for sIndex = 1:trial.setsize,
	SCREEN(visualInfo.stimulusPtr,'FillRect', trial.color(sIndex,:), rectangle(sIndex,:));
end;
elapsedtime = GetSecs - t; 
WaitSecs(expInfo.iti - elapsedtime);   

displayMessage(visualInfo, '+', false);  %fixation cross
WaitSecs(expInfo.startinterval);

SCREEN(visualInfo.mainPtr,'FillRect');               %wipe out the cue, JIK

%tic

SCREEN('CopyWindow',visualInfo.stimulusPtr,visualInfo.mainPtr);            % copy the off screen display into standard display
 WaitSecs(expInfo.displaytime);

SCREEN(visualInfo.mainPtr,'FillRect');
%toc

WaitSecs(expInfo.delay);

SCREEN('CopyWindow',visualInfo.targetPtr,visualInfo.mainPtr);            % copy the color wheel + probe into standard display

% get response from participant
[trial.pressedKey, trial.RT, trial.correctness] = getResponse(trial.correctResponse, expInfo, autoPilot)

SCREEN(visualInfo.mainPtr,'FillRect');
SCREEN(visualInfo.targetPtr, 'FillRect');
SCREEN(visualInfo.colorwheelPtr, 'FillRect');
SCREEN(visualInfo.stimulusPtr, 'FillRect');