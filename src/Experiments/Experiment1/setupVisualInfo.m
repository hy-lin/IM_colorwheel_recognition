function visualInfo = setupVisualInfo()

visualInfo.fgColor = 0;
visualInfo.bgColor = 255;
visualInfo.probeColor = [0 0 255];
visualInfo.stimuliColro = [255 0 0];
visualInfo.fontName = 'MingLiU';
visualInfo.fontSize = 40;

[visualInfo.mainPtr visualInfo.windowsRect]= Screen(0, 'OpenWindow', visualInfo.bgColor);
visualInfo.colorwheelPtr = Screen(visualInfo.mainPtr, 'OpenoffscreenWindow', visualInfo.bgColor);
visualInfo.targetPtr = Screen(visualInfo.mainPtr, 'OpenoffscreenWindow', visualInfo.bgColor);
visualInfo.stimulusPtr = Screen(visualInfo.mainPtr, 'OpenoffscreenWindow', visualInfo.bgColor);
visualInfo.offPtr = Screen(visualInfo.mainPtr, 'OpenoffscreenWindow', visualInfo.bgColor);

Screen(visualInfo.mainPtr, 'TextSize', visualInfo.fontSize);
Screen(visualInfo.mainPtr, 'TextFont', visualInfo.fontName);
Screen(visualInfo.colorwheelPtr, 'TextSize', visualInfo.fontSize);
Screen(visualInfo.colorwheelPtr, 'TextFont', visualInfo.fontName);
Screen(visualInfo.targetPtr, 'TextSize', visualInfo.fontSize);
Screen(visualInfo.targetPtr, 'TextFont', visualInfo.fontName);
Screen(visualInfo.stimulusPtr, 'TextSize', visualInfo.fontSize);
Screen(visualInfo.stimulusPtr, 'TextFont', visualInfo.fontName);
Screen(visualInfo.offPtr, 'TextSize', visualInfo.fontSize);
Screen(visualInfo.offPtr, 'TextFont', visualInfo.fontName);

visualInfo.centerofX = visualInfo.windowsRect(3) / 2;
visualInfo.centerofY = visualInfo.windowsRect(4) / 2;

visualInfo.penWidth = 2;
visualInfo.frameWidth = 40;
visualInfo.frameHeight = 40;

visualInfo.L = 70;
visualInfo.a = 20;
visualInfo.b = 38;