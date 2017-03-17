function displayMessage(visualInfo, msg, keypress)

Screen(visualInfo.offPtr, 'FillRect', visualInfo.bgColor);
x = visualInfo.centerofX - Screen(visualInfo.offPtr, 'TextWidth', msg) / 2;
y = visualInfo.centerofY - Screen(visualInfo.offPtr, 'TextWidth', '  ') / 2;
Screen(visualInfo.offPtr, 'DrawText', msg, x, y, visualInfo.fgColor);
Screen('CopyWindow', visualInfo.offPtr, visualInfo.mainPtr);

WaitSecs(.1);

if keypress,
	while 1,
		keyIsDown = kbCheck();
		if keyIsDown,
			break;
		end;
	end;
end;