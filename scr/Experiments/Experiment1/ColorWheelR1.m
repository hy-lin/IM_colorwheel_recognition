function localRecognition4(pid, session, autoPilot, debug)
% The local recognition task with two parts.
% Syntax:
%	 localRecognition(participantID, participantSession)
% Description
%	 participantID is the index number of the participant, and the participantSession is the current session of the participant. Ex: localRecognition(89, 3) for the third session of participant 89.
% This is the program written by Hsuan-Yu Lin, latest modification at 10, Sep, 2012. 

if nargin < 1,
	error('Please input participant ID');
end;

if nargin < 2,
	error('Please input session');
end;

if nargin < 4,
	debug = false;
end;

if nargin < 3,
	autoPilot = false;
end;

rSeed = sum(100*clock);
RandStream.setDefaultStream(RandStream('mt19937ar','seed',rSeed));

expInfo = setupExpInfo(debug);
visualInfo = setupVisualInfo();

practiceTrialInfo = setupPracticeTrialInfo(visualInfo, expInfo);
expTrialInfo = setupExpTrialInfo(visualInfo, expInfo);

fid = fopen('experimentLog.log', 'a');
	t = clock;
	fprintf(fid, '%s %d:%d:%d \t', date, t(4), t(5), ceil(t(6)));
	fprintf(fid, '%d\t%d\t%.2f\n', pid, session, rSeed);
fclose(fid);

HideCursor;

displayMessage(visualInfo, expInfo.practiceBegins, true);
for practiceTrialIndex = 1:length(practiceTrialInfo),
	DisplayTrial1(visualInfo, expInfo, practiceTrialInfo(practiceTrialIndex), autoPilot);
end;

displayMessage(visualInfo, expInfo.experimentBegins, true);
for expTrialIndex = 1:length(expTrialInfo),
	expTrialInfo(expTrialIndex) = DisplayTrial1(visualInfo, expInfo, expTrialInfo(expTrialIndex), autoPilot);
	saveTrialInfo(expTrialInfo(expTrialIndex), expInfo, pid, session, expTrialIndex);
	
	if mod(expTrialIndex, 30) == 0,
		displayMessage(visualInfo, expInfo.breakBegins, true);
	end;
end;


displayMessage(visualInfo, expInfo.experimentEnds, true);

ShowCursor;

Screen('CloseAll');