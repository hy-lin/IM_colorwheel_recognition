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
  
  data$Response <- factor(data$Response)
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
  data$ProbeType <- 1
  data$dissimilarity <- 1
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
          }else{
            data$Correctness[i] <- 0
          }
        }else{
          if (data$Response[i] == 'True'){
            data$Correctness[i] <- 0
          }else{
            data$Correctness[i] <- 1
          }
        }
      }else{
        data$Correctness[i] <- wrapDistance(data$ColorTarget[i], data$ColorProbe[i])
      }
    }
    
  }
  data$ProbeType <- factor(data$ProbeType)
  return(data)
}

#getCorrectness <- function(data){
#  data$Correctness <- -1
#  for (i in 1:length(data$TrialIndex)){
#    if 
#  }
#  
#}

exp3.data <- loadData(3)
exp3.data <- classifyProbeType(exp3.data, 3)


data <- data.frame(aggregate(list(exp2.data$Correctness, exp2.data$RT, exp2.data$SimPC), list(exp2.data$ID, exp2.data$ProbeType, exp2.data$Setsize), mean))
names(data) <- c('ID', 'ProbeType', 'Setsize', 'PC', 'RT', 'IM')

tmp_data <- data.frame(aggregate(list(data$PC, data$RT, data$IM), list(data$ProbeType, data$Setsize), mean))
tmp_data_sd <- data.frame(aggregate(list(data$PC, data$RT), list(data$ProbeType, data$Setsize), sd))
tmp_data[, 6] <- tmp_data_sd[, 3] / sqrt(20)
tmp_data[, 7] <- tmp_data_sd[, 4] / sqrt(20)
names(tmp_data) <- c('ProbeType', 'Setsize', 'PC', 'RT', 'IM', 'PC_SE', 'RT_SE')
pd <- position_dodge(.1)
ggplot(data=tmp_data) + aes(x=Setsize, y = PC, linetype = ProbeType) + 
  geom_line(position = pd, size = 1) + 
  geom_errorbar(aes(ymin=PC-PC_SE, ymax=PC+PC_SE), width=.1, position = pd, size = 1) + 
  geom_point(position = pd, size = 1) +
  geom_line(position = pd, aes(x=Setsize, y = IM, linetype = ProbeType, group = ProbeType), color = 'red', size = 1) +
  xlab('Set Size') +
  ylab('Propotion of Correct') +
  theme(text = element_text(size=14)) +
  theme(legend.text = element_text(size=14))

pd <- position_dodge(.1)
ggplot(data=tmp_data) + aes(x=Setsize, y = PC, linetype = ProbeType) + 
  geom_line(position = pd, size = 1) + 
  geom_errorbar(aes(ymin=PC-PC_SE, ymax=PC+PC_SE), width=.1, position = pd, size = 1) + 
  geom_point(position = pd, size = 1) +
  xlab('Set Size') +
  ylab('Propotion of Correct') +
  theme(legend.text = element_text(size = 20))

pd <- position_dodge(.1)
ggplot(data=tmp_data) + aes(x=Setsize, y = RT, linetype = ProbeType, group = ProbeType) + 
  geom_line(position = pd, size = 1) + 
  geom_errorbar(aes(ymin=RT-RT_SE, ymax=RT+RT_SE), width=.1, position = pd, size = 1) + 
  geom_point(position = pd, size = 1) +
  xlab('Set Size') +
  ylab('Reaction Time (s)')

bins <- seq(0, 180, 20)
h1 <- hist(x = exp2.data[exp2.data$Setsize==6 & exp2.data$Response==0,]$dissimilarity, breaks = bins, plot = 0)
h2 <- hist(x = exp2.data[exp2.data$Setsize==6,]$dissimilarity, breaks = bins, plot = 0)

IM_dist <- rep(0, 9)
for (i in 1:9){
  IM_dist[i] <- 1- mean(exp2.data[exp2.data$Setsize==6 & exp2.data$dissimilarity >= bins[i] & exp2.data$dissimilarity < bins[i+1],]$IM)
}

tmp_data <- data.frame(cbind(bins[-10], h1$counts/h2$counts, IM_dist))
names(tmp_data) <- c('breaks', 'frequency', 'IM')

ggplot(data=tmp_data)+aes(breaks, frequency)+
  geom_col() +
  ylim(0, 1) +
  xlab('Similarity between target and probe') +
  ylab('Proportion of "no change" response') +
  geom_line(aes(breaks, IM), color = 'red', size = 2) +
  theme(text = element_text(size=14))
