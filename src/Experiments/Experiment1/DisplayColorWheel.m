function shift = DisplayColorWheel(visualInfo, window, trialInfo, shift)

if nargin < 4, % for unknown reason that I forget to put shift as input
	s = 1;   % shift is fixed to one in colorwheel r, since the colorwheel only exists for debugging reason.
	shift = (1:360) + s(1);   %random rotation of color wheel
	shift(shift>360) = shift(shift > 360)-360;
end;

maxrect=SCREEN(window,'Rect');
maxx = maxrect(3); maxy = maxrect(4);

%%% computes RGB values for 360 positions on the color wheel, 

for ang = 1:360
    RGB(ang,:) = Angle2RGB(ang, visualInfo.L, visualInfo.a, visualInfo.b);
end

X = maxx/2; Y = maxy/2;
radius1 = maxy/2.5;
radius2 = radius1 + maxy/20;
for ang = 1:361
    a = 2*pi*ang/360;
    if ang > 360, a = 2*pi/360; end
    x1(ang) = X + radius1 * cos(a);
    y1(ang) = Y + radius1 * sin(a);
    x2(ang) = X + radius2 * cos(a);
    y2(ang) = Y + radius2 * sin(a);
end

for ang = 1:360
    pointlist = [x1(ang), y1(ang); x2(ang), y2(ang); x2(ang+1) y2(ang+1); x1(ang+1), y1(ang+1)];
    Screen(window, 'FillPoly', RGB(shift(ang),:), pointlist);
end

ang = trialInfo.cang(1);
pointlist = [x1(ang), y1(ang); x2(ang), y2(ang); x2(ang+1) y2(ang+1); x1(ang+1), y1(ang+1)];
Screen(window, 'FillPoly', 255, pointlist);

for i = 2:trialInfo.setsize,
	ang = trialInfo.cang(i)
	pointlist = [x1(ang), y1(ang); x2(ang), y2(ang); x2(ang+1) y2(ang+1); x1(ang+1), y1(ang+1)];
	Screen(window, 'FillPoly', 0, pointlist);
end;

