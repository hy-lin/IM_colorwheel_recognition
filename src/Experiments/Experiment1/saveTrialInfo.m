function saveTrialInfo(trialInfo, expInfo, pid, session, expTrialIndex)

fid = fopen(expInfo.saveFile, 'a');

fprintf(fid, '%d\t', pid, session, expTrialIndex);
fprintf(fid, '%d\t', trialInfo.setsize);
for i = 1:max(expInfo.setsize),
	fprintf(fid, '%d\t%d\t', trialInfo.cang(i), trialInfo.pang(i));
end;

fprintf(fid, '%d\t', trialInfo.probeType, trialInfo.probeAng);
fprintf(fid, '%d\t', trialInfo.pressedKey);
fprintf(fid, '%.4f\t%d\n', trialInfo.RT, trialInfo.correctness);

fclose(fid);