function expInfo = setupExpInfo(debug)

expInfo.numberofPracticeTrialsPerBlock = 2;
expInfo.numberofExpTrialsPerBlock      = 70;

expInfo.saveFile = 'Data\\colorwheelr1.dat';

expInfo.practiceBegins = 'Damit die Übungsphase startet, drücke bitte die Leertaste';
expInfo.experimentBegins = 'Damit das Experiment beginnt, drücke bitte die Leertaste';
expInfo.experimentEnds = 'Ende des Experiments, informiere bitte den Versuchsleiter';
expInfo.breakBegins = 'Kurze Pause, weiter mit der Leertaste';

expInfo.validKey = {'left', 'right'};
expInfo.escapeKey = {'F12'};

expInfo.startinterval                  = 0.5;          %interval between fixation cross and memory display
expInfo.displaytime                    = .1;           %display time of memory items (color patches)
expInfo.setsize                        = 1:6;          %range of set sizes
expInfo.delay                          = 1;            %range of retention interval before recall
expInfo.iti                            = 2.5;          %inter-trial interval
expInfo.npos                           = 13;           %number of different spatial positions on the virtual circle
expInfo.PauseAfterBreak                = 2;

expInfo.probeTypeRatio                 = [.5 .25 .25]; % positive probe, negative probe, intrusion probe
expInfo.precision                      = [10.3619, 13.6784, 15.7248, 16.9642, 18.2413, 17.4550];

expInfo.debug = debug