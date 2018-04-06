library(ggplot2)
library(BayesFactor)

loadData <- function(exp){
  if (exp == 1 | exp == 2){
    data <- read.table(sprintf('Data/Experiment%d/recognition%d.dat', exp, exp), header = FALSE, fill = FALSE)
    names(data) <- c('ID', 'TrialIndex', 'Setsize', 'TrialCondition',
                     'ColorTarget', 'LocationTarget',
                     'ColorNonTarget1', 'LocationNonTarget1',
                     'ColorNonTarget2', 'LocationNonTarget2',
                     'ColorNonTarget3', 'LocationNonTarget3',
                     'ColorNonTarget4', 'LocationNonTarget4',
                     'ColorNonTarget5', 'LocationNonTarget5',
                     'ColorProbe', 'LocationProbe',
                   'Response', 'Correctness', 'RT')
    data$TrialCondition <- factor(data$TrialCondition)
  }
  
  if (exp == 3){
    data <- read.table('Data/Experiment3/recallNrecognition.dat', header = FALSE, fill = FALSE)
    names(data) <- c('ID', 'Session', 'SessionCondition',
                    'TrialIndex', 'TrialType', 'Setsize',
                    'ProbeType', 'ColorTarget', 'LocationTarget',
                    'ColorNonTarget1', 'LocationNonTarget1',
                    'ColorNonTarget2', 'LocationNonTarget2',
                    'ColorNonTarget3', 'LocationNonTarget3',
                    'ColorNonTarget4', 'LocationNonTarget4',
                    'ColorNonTarget5', 'LocationNonTarget5',
                    'ColorProbe', 'LocationProbe',
                    'RT', 'Response'
                    )
  }
  
  data$ID <- factor(data$ID)
  data$TrialIndex <- factor(data$TrialIndex)
  
  #data$Response <- factor(data$Response)
  return(data)
}

loadSimulationData <- function(exp){
  data <- read.table(sprintf('Data/fitting result/exp%d.dat', exp, exp), header = FALSE, fill = FALSE)
  names(data) <- c('ID', 'TrialIndex', 'Setsize', 'TrialCondition',
                   'ColorTarget', 'LocationTarget',
                   'ColorNonTarget1', 'LocationNonTarget1',
                   'ColorNonTarget2', 'LocationNonTarget2',
                   'ColorNonTarget3', 'LocationNonTarget3',
                   'ColorNonTarget4', 'LocationNonTarget4',
                   'ColorNonTarget5', 'LocationNonTarget5',
                   'ColorProbe', 'LocationProbe',
                   'Response', 'Correctness', 'RT',
                   'IM', 'SA', 'SB-Binding', 'VP', 'VP-Binding')
  data$ID <- factor(data$ID)
  data$TrialIndex <- factor(data$TrialIndex)
  data$TrialCondition <- factor(data$TrialCondition)
  data$Response <- factor(data$Response)
  return(data)
}

wrapDistance <- function(color1, color2){
  dist <- abs(color1-color2)
  if (dist >= 180){
    dist <- 360 - dist
  }
  return(dist)
}

classifyProbeType <- function(data, exp){
  bins <- seq(0, 180, 20)
  data$ProbeType <- 1
  data$dissimilarity <- 1
  data$dissimilarity_bin <- 1
  for (i in 1:length(data$ProbeType)){
    if (exp == 1 | exp == 2){
      if (data$ColorProbe[i] == data$ColorTarget[i]){
        data$ProbeType[i] = 'Same'
        data$SimPC[i] = 1-data$IM[i]
      }
      else {
        intrusion = FALSE
        if (data$Setsize[i] > 1){
          for (l in 1:(data$Setsize[i]-1)){
            nontargetvar <- sprintf('ColorNonTarget%d', l)
            if (wrapDistance(data$ColorProbe[i], data[i, nontargetvar]) < 13){
              intrusion = TRUE
            }
          }
        }
        
        if (intrusion == TRUE){
          data$ProbeType[i] = 'Internal Change'
        } else{
          data$ProbeType[i] = 'External Change'
        }
        data$SimPC[i] = data$IM[i]
      }
      
      data$dissimilarity[i] <- wrapDistance(data$ColorProbe[i], data$ColorTarget[i])
      data$dissimilarity_bin[i] <- which.max(data$dissimilarity[i] <= bins)
    }
    else{
      if (data$TrialType[i] == 'recognition'){
        if (data$ColorProbe[i] == data$ColorTarget[i]){
          data$ProbeType[i] = 'Same'
          data$SimPC[i] = 1-data$IM[i]
        }
        else {
          intrusion = FALSE
          if (data$Setsize[i] > 1){
            for (l in 1:(data$Setsize[i]-1)){
              nontargetvar <- sprintf('ColorNonTarget%d', l)
              if (wrapDistance(data$ColorProbe[i], data[i, nontargetvar]) < 13){
                intrusion = TRUE
              }
            }
          }
          
          if (intrusion == TRUE){
            data$ProbeType[i] = 'Internal Change'
          } else{
            data$ProbeType[i] = 'External Change'
          }
          data$SimPC[i] = data$IM[i]
        }
        if (data$ProbeType[i] == 'Same'){
          if (data$Response[i] == 'True'){
            data$Correctness[i] <- 1
            data$Response[i] = 1
          }else{
            data$Correctness[i] <- 0
            data$Response[i] = 0
          }
        }else{
          if (data$Response[i] == 'True'){
            data$Correctness[i] <- 0
            data$Response[i] = 1
          }else{
            data$Correctness[i] <- 1
            data$Response[i] = 0
          }
        }
        data$dissimilarity[i] <- wrapDistance(data$ColorProbe[i], data$ColorTarget[i])
        data$dissimilarity_bin[i] <- which.max(data$dissimilarity[i] <= bins)
      }else{
        data$Correctness[i] <- wrapDistance(data$ColorTarget[i], data$ColorProbe[i])
        data$dissimilarity_bin[i] <- which.max(data$Correctness[i] <= bins)
      }
    }
    
  }
  data$ProbeType <- factor(data$ProbeType)
  return(data)
}


exp3.data <- loadData(3)
exp3.data <- classifyProbeType(exp3.data, 3)

data <- data.frame(aggregate(list(exp3.data$Correctness, exp3.data$RT), list(exp3.data$ID,exp3.data$TrialType, exp3.data$SessionCondition, exp3.data$ProbeType, exp3.data$Setsize), mean))
names(data) <- c('ID','TrialType', 'SessionCondition', 'ProbeType', 'Setsize', 'PC', 'RT')

tmp_data <- data.frame(aggregate(list(data[data$TrialType!='recall',]$PC, data[data$TrialType!='recall',]$RT), list(data[data$TrialType!='recall',]$ProbeType, data[data$TrialType!='recall',]$Setsize), mean))
tmp_data_sd <- data.frame(aggregate(list(data[data$TrialType!='recall',]$PC, data[data$TrialType!='recall',]$RT), list(data[data$TrialType!='recall',]$ProbeType, data[data$TrialType!='recall',]$Setsize), sd))
tmp_data[, 5] <- tmp_data_sd[, 3] / sqrt(20)
tmp_data[, 6] <- tmp_data_sd[, 4] / sqrt(20)
names(tmp_data) <- c('ProbeType', 'Setsize', 'PC', 'RT', 'PC_SE', 'RT_SE')
pd <- position_dodge(.1)
ggplot(data=tmp_data) + aes(x=Setsize, y = PC, linetype = ProbeType) + 
  geom_line(position = pd, size = 1) + 
  geom_errorbar(aes(ymin=PC-PC_SE, ymax=PC+PC_SE), width=.1, position = pd, size = 1) + 
  geom_point(position = pd, size = 1) +
#  geom_line(position = pd, aes(x=Setsize, y = IM, linetype = ProbeType, group = ProbeType), color = 'red', size = 1) +
  xlab('Set Size') +
  ylab('Propotion of Correct')

pd <- position_dodge(.1)
ggplot(data=tmp_data) + aes(x=Setsize, y = RT, linetype = ProbeType, group = ProbeType) + 
  geom_line(position = pd, size = 1) + 
  geom_errorbar(aes(ymin=RT-RT_SE, ymax=RT+RT_SE), width=.1, position = pd, size = 1) + 
  geom_point(position = pd, size = 1) +
  xlab('Set Size') +
  ylab('Reaction Time (s)')

tmp_data <- data.frame(aggregate(list(data[data$TrialType!='recall',]$PC, data[data$TrialType!='recall',]$RT), list(data[data$TrialType!='recall',]$ProbeType, data[data$TrialType!='recall',]$SessionCondition, data[data$TrialType!='recall',]$Setsize), mean))
tmp_data_sd <- data.frame(aggregate(list(data[data$TrialType!='recall',]$PC, data[data$TrialType!='recall',]$RT), list(data[data$TrialType!='recall',]$ProbeType, data[data$TrialType!='recall',]$SessionCondition, data[data$TrialType!='recall',]$Setsize), sd))
tmp_data[, 6] <- tmp_data_sd[, 4] / sqrt(20)
tmp_data[, 7] <- tmp_data_sd[, 5] / sqrt(20)
names(tmp_data) <- c('ProbeType', 'SessionCondition', 'Setsize', 'PC', 'RT', 'PC_SE', 'RT_SE')
pd <- position_dodge(.25)
ggplot(data=tmp_data) + aes(x=Setsize, y = PC, linetype = ProbeType, color = SessionCondition) + 
  geom_line(position = pd, size = 1) + 
  geom_errorbar(aes(ymin=PC-PC_SE, ymax=PC+PC_SE), width=.1, position = pd, size = 1) + 
  geom_point(position = pd, size = 1) +
  #  geom_line(position = pd, aes(x=Setsize, y = IM, linetype = ProbeType, group = ProbeType), color = 'red', size = 1) +
  xlab('Set Size') +
  ylab('Propotion of Correct') +
  scale_color_manual(values = c(mix = 'black', recognition = 'gray')) +
  theme_bw()

pd <- position_dodge(.1)
ggplot(data=tmp_data) + aes(x=Setsize, y = RT, linetype = ProbeType, color = SessionCondition) + 
  geom_line(position = pd, size = 1) + 
  geom_errorbar(aes(ymin=RT-RT_SE, ymax=RT+RT_SE), width=.1, position = pd, size = 1) + 
  geom_point(position = pd, size = 1) +
  xlab('Set Size') +
  ylab('Reaction Time (s)') 

tmp_data <- data.frame(
  aggregate(list(as.numeric(exp3.data[exp3.data$TrialType!='recall',]$Response)-2),
            list(exp3.data[exp3.data$TrialType!='recall',]$dissimilarity_bin, exp3.data[exp3.data$TrialType!='recall',]$Setsize, exp3.data[exp3.data$TrialType!='recall',]$SessionCondition),
            mean, 
            na.action = na.omit)
)
names(tmp_data) <- c('breaks', 'setsize', 'SessionCondition', 'frequency')
tmp_data$setsize <- factor(tmp_data$setsize)
tmp_data$breaks <- tmp_data$breaks / 10 * 180

pd <- position_dodge(.1)
ggplot(data=tmp_data) + aes(x=breaks, y = frequency, linetype = setsize, color = SessionCondition) + 
  geom_line(position = pd, size = 1) + 
  geom_point(position = pd, size = 1) +
  xlab('Target-probe similarity') +
  ylab('Propotion of Same')