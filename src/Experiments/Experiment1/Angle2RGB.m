function RGB = Angle2RGB(ang, L, a, b, radius)
% computes RGB color code for a color wheel from the angle (1 to 360) with CIELab colorspaces,
% the function uses the algorism from David Anderson. 
% for future detail, refert to Wikipedia: SRGB
%
% Usage:
% RGB = Angle2RGB(ang, L, a, b, radius=60)
% 	ang is the angle on the color wheel. 
% 	L, a, b are the central coordinates for CIELab color space.
% 	radius is the radius from the central coordinates
%  	The common values of L, a, and b are 70, 20, and 38, respectively. 

	if nargin < 5,
		radius = 60;
	end;

	theta = ang * pi / 180; % convert angle to radian
	A = a + radius*cos(theta); % create the list of A for different angles on the wheel
	B = b + radius*sin(theta); % create the list of B for different angles on the wheel
	L = repmat(L, size(A)); % L remains constant to all the angle on the wheel
	
	% convert Lab to XYZ
	var_Y = (L + 16) ./ 115;
	var_X = A ./ 500 + var_Y;
	var_Z = var_Y - B ./ 200;
	
	% filter X, Y, Z with threshold 0.008856
	threshold_passes = (var_Y .^ 3) > 0.008856;
	var_Y(threshold_passes) = var_Y(threshold_passes) .^ 3;
	var_Y(~threshold_passes) = (var_Y(~threshold_passes) - 16 / 116) / 7.787;
	threshold_passes = (var_X .^ 3) > 0.008856;
	var_X(threshold_passes) = var_X(threshold_passes) .^ 3;
	var_X(~threshold_passes) = (var_X(~threshold_passes) - 16 / 116) / 7.787;
	threshold_passes = (var_Z .^ 3) > 0.008856;
	var_Z(threshold_passes) = var_Z(threshold_passes) .^ 3;
	var_Z(~threshold_passes) = (var_Z(~threshold_passes) - 16 / 116) / 7.787;
	
	% define reference points
    ref_X =  95.047; 
    ref_Y = 100.000;
    ref_Z = 108.883;
	
	% rescale X, Y, Z according to reference points
	X = ref_X .* var_X ./ 100;
	Y = ref_Y .* var_Y ./ 100;
	Z = ref_Z .* var_Z ./ 100;
	
	% convert X, Y, Z to RGB
	var_R = X .*  3.2406 + Y .* -1.5372 + Z .* -0.4986;
	var_G = X .* -0.9689 + Y .*  1.8758 + Z .*  0.0415;
	var_B = X .*  0.0557 + Y .* -0.2040 + Z .*  1.0570;
	
	% gamma correction to IEC 61966-2-1 standard
	threshold_passes = var_R > 0.0031308;
	R(threshold_passes) = 1.055 .* (var_R(threshold_passes) .^ (1/2.4)) - 0.055;
	R(~threshold_passes) = 12.92 .* var_R(~threshold_passes);
	threshold_passes = var_G > 0.0031308;
	G(threshold_passes) = 1.055 .* (var_G(threshold_passes) .^ (1/2.4)) - 0.055;
	G(~threshold_passes) = 12.92 .* var_G(~threshold_passes);
	threshold_passes = var_B > 0.0031308;
	B(threshold_passes) = 1.055 .* (var_B(threshold_passes) .^ (1/2.4)) - 0.055;
	B(~threshold_passes) = 12.92 .* var_B(~threshold_passes);
	
	RGB = [R;G;B] .* 255;
    % Trimming
    RGB(RGB>255) = 255;
    RGB(RGB<0) = 0;
    RGB = RGB';
end