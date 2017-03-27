function trial = setupPracticeTrialInfo(visualInfo, expInfo)

tInd = 0;

for szInd = expInfo.setsize,

	% assign probe type to each trials
	randNum = randperm(3);
	probeTypePool = randNum(1:expInfo.numberofPracticeTrialsPerBlock);

		
	if expInfo.setsize(szInd) == 1,
		% no intrusion probe in set size 1, replaced with negative probe
		probeTypePool(probeTypePool == 3) = 2;
	end;

	for repInd = 1:expInfo.numberofPracticeTrialsPerBlock,
		tInd = tInd + 1;
		
		trial(tInd).setsize = expInfo.setsize(szInd);
		
		trial(tInd).pressedKey = 0;
		trial(tInd).RT = 0;
		trial(tInd).correctness = -1;
		
		maxx = visualInfo.windowsRect(3);
		maxy = visualInfo.windowsRect(4);
		radius = maxy/4;

		X = maxx/2; Y = maxy/2;
		c = randperm(360);
		trial(tInd).cang = c(1:max(expInfo.setsize));  %color angles (1 to 360 on standard, unrotated color wheel) - always produces maximum number of objects for saving
		for i = 1:length(trial(tInd).cang)
			trial(tInd).color(i,:) = Angle2RGB(trial(tInd).cang(i), visualInfo.L, visualInfo.a, visualInfo.b);
		end

		p = randperm(expInfo.npos);  %npos equally spaced positions
		trial(tInd).pang = p(1:max(expInfo.setsize));   %position angles (numbered 1 to npos)
		trial(tInd).coordx = X + radius * cos(2*pi*trial(tInd).pang/expInfo.npos);  
		trial(tInd).coordy = Y + radius * sin(2*pi*trial(tInd).pang/expInfo.npos);

		% determine probe
		trial(tInd).probeType = probeTypePool(repInd);
		
		switch trial(tInd).probeType
			case 1, % positive probe
				trial(tInd).probeAng = (rand - .5) * expInfo.precision(szInd) * 2 + trial(tInd).cang(1);
				trial(tInd).correctResponse = 2;
				
			case 2, % negative probe
				% This is a little bit complecate. 
				avaliable = ones(1, 360); % the avaliablity of all colors
				
				for i = 1:trial(tInd).setsize,
					occupied = trial(tInd).cang(i) + ceil((-expInfo.precision(szInd)):1:expInfo.precision(szInd));
					% wrapping occupied
					occupied(occupied <= 0) = 360 + occupied(occupied <= 0);
					occupied(occupied > 360) = occupied(occupied > 360) - 360;
					
					avaliable(occupied) = 0; % remove the unavaliable colors.
				end;
				
				% magic!
				pickedInd = ceil(rand * sum(avaliable));  
				[~, ind] = sort(avaliable, 2, 'descend');
				
				trial(tInd).probeAng = ind(pickedInd);
				trial(tInd).correctResponse = 1;
				
			case 3, % intrusion probe
				% randomly select one distractor. 
				distractor = ceil(rand*(trial(tInd).setsize-1)+1);
				trial(tInd).probeAng = (rand - .5) * expInfo.precision(szInd) * 2 + trial(tInd).cang(distractor);
				trial(tInd).correctResponse = 1;
		end;
		
		% wrap probe angle
		trial(tInd).probeAng = ceil(trial(tInd).probeAng);
		if trial(tInd).probeAng <= 0, trial(tInd).probeAng = 360 + trial(tInd).probeAng; end;
		if trial(tInd).probeAng > 360, trial(tInd).probeAng = trial(tInd).probeAng - 360; end;
		
		trial(tInd).probeColor = Angle2RGB(trial(tInd).probeAng, visualInfo.L, visualInfo.a, visualInfo.b);
		
	end;
end;

trial = shuffle(trial);