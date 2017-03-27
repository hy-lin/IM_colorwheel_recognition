function [pressedKey, RT, correctness] = getResponse(correctResponse, expInfo, autoPilot)

st = GetSecs();

while 1,
	[keyIsDown, ~, keyCode] = kbCheck();
	
	if autoPilot,
		keyIsDown = true;
	end;
	
	if keyIsDown, %auto run
		pressedKey = find(strcmp(upper(expInfo.validKey), upper(KbName(keyCode))));
		if autoPilot,
			pressedKey = 1;
			WaitSecs(1);
		end;
		if ~isempty(pressedKey) & length(pressedKey) < 2,
			RT = GetSecs() - st;
			if pressedKey == correctResponse,
				correctness = 1;
			else
				correctness = 0;
			end;
			return;
		end;
		if strcmp(upper(expInfo.escapeKey), upper(KbName(keyCode))),
			correctness = -1; % -1 means BAD! 
			pressedKey = -1;
			RT = -1; % you got three -1, really BAD!
			Screen('CloseAll');
			error('User terminated the program with escape key');
		end;
	end;
end;