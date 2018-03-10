library(ggplot2)
library(BayesFactor)

loadData <- function(exp){
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
  data$ID <- factor(data$ID)
  data$TrialIndex <- factor(data$TrialIndex)
  data$TrialCondition <- factor(data$TrialCondition)
  # data$Response <- factor(data$Response)
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
  #data$Response <- factor(data$Response)
  return(data)
}

wrapDistance <- function(color1, color2){
  dist <- abs(color1-color2)
  if (dist >= 180){
    dist <- 360 - dist
  }
  return(dist)
}

classifyProbeType <- function(data){
  bins <- seq(0, 180, 20)
  
  data$ProbeType <- 1
  data$dissimilarity <- 1
  data$dissimilarity_bin <- 1
  
  for (i in 1:length(data$ProbeType)){
    if (data$ColorProbe[i] == data$ColorTarget[i]){
      data$ProbeType[i] = 'Same'
      data$SimPC[i] = 1-data$'VP-Binding'[i]
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
      data$SimPC[i] = data$'VP-Binding'[i]
    }
    
    data$dissimilarity[i] <- wrapDistance(data$ColorProbe[i], data$ColorTarget[i])
    data$dissimilarity_bin[i] <- which.max(data$dissimilarity[i] <= bins)
    
  }
  data$ProbeType <- factor(data$ProbeType)
  return(data)
}

exp2.data <- loadSimulationData(2)
exp2.data <- classifyProbeType(exp2.data)
exp2.data$OldProbeType[exp2.data$TrialCondition=='intrusion'] = 'change'
exp2.data$OldProbeType[exp2.data$TrialCondition=='new'] = 'change'
exp2.data$OldProbeType[exp2.data$TrialCondition=='positive'] = 'same'

# 'SA', 'SB-Binding', 'VP', 'VP-Binding'
data <- data.frame(aggregate(
  list(exp2.data$Correctness,
       exp2.data$RT),
  list(exp2.data$ID, exp2.data$OldProbeType, exp2.data$Setsize),
  mean)
)
names(data) <- c('ID', 'OldProbeType', 'Setsize', 'PC', 'RT')


tmp_data <- data.frame(aggregate(list(data$PC), list(data$OldProbeType, data$Setsize), mean))
tmp_data_sd <- data.frame(aggregate(list(data$PC), list(data$OldProbeType, data$Setsize), sd))
tmp_data[, 4] <- tmp_data_sd[, 3] / sqrt(20)
names(tmp_data) <- c('ProbeType', 'Setsize', 'PC', 'PC_SE')
pd <- position_dodge(.1)
ggplot(data=tmp_data) + aes(x=Setsize, y = PC, linetype = ProbeType) + 
  geom_line(position = pd, size = 1) + 
  geom_errorbar(aes(ymin=PC-PC_SE, ymax=PC+PC_SE), width=.1, position = pd, size = 1) + 
  geom_point(position = pd, size = 1) +
  xlab('Set Size') +
  ylab('Propotion of Correct') +
  theme(text = element_text(size = 20)) +
  theme(legend.text = element_text(size = 20)) 



tmp_data <- data.frame(aggregate(list(data$PC, data$SimPC), list(data$ProbeType, data$Setsize), mean))
tmp_data_sd <- data.frame(aggregate(list(data$PC), list(data$ProbeType, data$Setsize), sd))
tmp_data[, 5] <- tmp_data_sd[, 3] / sqrt(20)
names(tmp_data) <- c('ProbeType', 'Setsize', 'PC', 'SimPC', 'PC_SE')
pd <- position_dodge(.1)
ggplot(data=tmp_data) + aes(x=Setsize, y = PC, linetype = ProbeType) + 
  geom_line(position = pd, size = 1) + 
  geom_errorbar(aes(ymin=PC-PC_SE, ymax=PC+PC_SE), width=.1, position = pd, size = 1) + 
  geom_point(position = pd, size = 1) +
  geom_line(position = pd, aes(x=Setsize, y = SimPC, linetype = ProbeType, group = ProbeType), color = 'red', size = 1) +
  xlab('Set Size') +
  ylab('Propotion of Correct') +
  theme(text = element_text(size = 20)) +
  theme(legend.text = element_text(size = 20))

pd <- position_dodge(.1)
ggplot(data=tmp_data) + aes(x=Setsize, y = PC, linetype = ProbeType) + 
  geom_line(position = pd, size = 1) + 
  geom_errorbar(aes(ymin=PC-PC_SE, ymax=PC+PC_SE), width=.1, position = pd, size = 1) + 
  geom_point(position = pd, size = 1) +
  xlab('Set Size') +
  ylab('Propotion of Correct') +
  theme(text = element_text(size = 20)) +
  theme(legend.text = element_text(size = 20)) 



# pd <- position_dodge(.1)
# ggplot(data=tmp_data) + aes(x=Setsize, y = RT, linetype = ProbeType, group = ProbeType) + 
#   geom_line(position = pd, size = 1) + 
#   geom_errorbar(aes(ymin=RT-RT_SE, ymax=RT+RT_SE), width=.1, position = pd, size = 1) + 
#   geom_point(position = pd, size = 1) +
#   xlab('Set Size') +
#   ylab('Reaction Time (s)')

tmp_data <- data.frame(
  aggregate(list(exp2.data$Response, exp2.data$'VP-Binding'),
            list(exp2.data$dissimilarity_bin, exp2.data$Setsize),
            mean, 
            na.action = na.omit)
)
names(tmp_data) <- c('breaks', 'setsize', 'frequency', 'IM')
tmp_data$setsize <- factor(tmp_data$setsize)
tmp_data$breaks <- tmp_data$breaks / 10 * 180

pd <- position_dodge(.1)
ggplot(data=tmp_data) + aes(x=breaks, y = 1-frequency, linetype = setsize) + 
  geom_line(position = pd, size = 1) + 
  geom_point(position = pd, size = 1) +
  xlab('Target-probe similarity') +
  ylab('Propotion of Same') +
  theme(text = element_text(size = 20)) +
  theme(legend.text = element_text(size = 20))

pd <- position_dodge(.1)
ggplot(data=tmp_data) + aes(x=breaks, y = 1-frequency, linetype = setsize) + 
  geom_line(position = pd, size = 1) + 
  geom_point(position = pd, size = 1) +
  geom_line(position = pd, aes(x=breaks, y = 1-IM, linetype = setsize), color = 'red', size = 1) +
  xlab('Target-probe similarity') +
  ylab('Propotion of Same') +
  theme(text = element_text(size = 20)) +
  theme(legend.text = element_text(size = 20))

tmp_data <- tmp_data[tmp_data$setsize %in% c(1, 3, 6), ]

pd <- position_dodge(.1)
ggplot(data=tmp_data) + aes(x=breaks, y = 1-frequency, linetype = setsize) + 
  geom_line(position = pd, size = 1) + 
  geom_point(position = pd, size = 1) +
  geom_line(position = pd, aes(x=breaks, y = 1-IM, linetype = setsize), color = 'red', size = 1) +
  xlab('Target-probe similarity') +
  ylab('Propotion of Same') +
  theme(text = element_text(size = 20)) +
  theme(legend.text = element_text(size = 20))
