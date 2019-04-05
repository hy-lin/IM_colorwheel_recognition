library(ggplot2)
library(BayesFactor)
library(jtools)
library(cowplot)

loadData <- function(exp){
  if (exp == 1){
    data <- read.table(sprintf('Data/Experiment%d/recognition%d.dat', exp, exp), header = FALSE, fill = FALSE)
    names(data) <- c('ID', 'SessionIndex', 'TrialIndex', 'Setsize', 
                     'ColorTarget', 'LocationTarget',
                     'ColorNonTarget1', 'LocationNonTarget1',
                     'ColorNonTarget2', 'LocationNonTarget2',
                     'ColorNonTarget3', 'LocationNonTarget3',
                     'ColorNonTarget4', 'LocationNonTarget4',
                     'ColorNonTarget5', 'LocationNonTarget5',
                     'TrialCondition', 'ColorProbe',
                     'Response', 'RT', 'Correctness')
    data$TrialCondition <- factor(data$TrialCondition)
  }
  if (exp == 2){
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
  
  #data$ID <- factor(data$ID)
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
  #data$ID <- factor(data$ID)
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
  if (dist == 180){
    dist <- 0
  }
  return(dist)
}

classifyProbeType <- function(data, exp){
  data$ProbeType <- 1
  data$dissimilarity <- 1
  data$exp <- 1
  for (i in 1:length(data$ProbeType)){
    
    if (exp == 2 | exp == 1){
      if (exp == 1){
        if (data$TrialCondition[i] == 1){
          data$ProbeType[i] = 'same'
        }else{
          if (data$TrialCondition[i] == 2){
            data$ProbeType[i] = 'new'
          }
          else{
            data$ProbeType[i] = 'intrusion'
          }
        }
        
        data$dissimilarity[i] <- wrapDistance(data$ColorProbe[i], data$ColorTarget[i])
        data$exp <- 1
        data$ID[i] <- data$ID[i] + 100
      }else{
      
        if (data$ColorProbe[i] == data$ColorTarget[i]){
          data$ProbeType[i] = 'same'
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
            data$ProbeType[i] = 'intrusion'
          } else{
            data$ProbeType[i] = 'new'
          }
          data$SimPC[i] = data$IM[i]
        }
        
        data$dissimilarity[i] <- wrapDistance(data$ColorProbe[i], data$ColorTarget[i])
        data$exp <- 2
        data$ID[i] <- data$ID[i] + 200
      }
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
  data$exp <- factor(data$exp)
  return(data)
}

#getCorrectness <- function(data){
#  data$Correctness <- -1
#  for (i in 1:length(data$TrialIndex)){
#    if 
#  }
#  
#}

# exp3.data <- loadData(3)
# exp3.data <- classifyProbeType(exp3.data, 3)

exp2.data <- loadData(2)
exp2.data <- classifyProbeType(exp2.data, 2)
exp2.data$LocationProbe <- NULL

exp1.data <- loadData(1)
exp1.data <- classifyProbeType(exp1.data, 1)
exp1.data$SessionIndex <- NULL

exp.data <- rbind(exp1.data, exp2.data)
exp.data$ID <- factor(exp.data$ID)

data <- data.frame(aggregate(list(exp.data$Correctness, exp.data$RT), list(exp.data$ID, exp.data$exp, exp.data$ProbeType, exp.data$Setsize), mean))
names(data) <- c('ID', 'Exp', 'ProbeType', 'Setsize', 'PC', 'RT')

# Exp effect
exp0 <- lmBF(PC ~ ID + ProbeType*Setsize, whichRandom = 'ID', data = data)
exp1 <- lmBF(PC ~ ID + ProbeType*Setsize*Exp, whichRandom = 'ID', data = data)

exp0/exp1

# Probetype * Setsize
no.effect <- lmBF(PC ~ ID, whichRandom = 'ID', data = data)
setsize <- lmBF(PC ~ Setsize + ID, whichRandom = 'ID', data = data)
probetype <- lmBF(PC ~ ProbeType + ID, whichRandom = 'ID', data = data)
probetype.setsize <- lmBF(PC ~ Setsize + ProbeType + ID, whichRandom = 'ID', data = data)
interaction <- lmBF(PC ~ Setsize*ProbeType + ID, whichRandom = 'ID', data = data)

#### setsize
setsize/no.effect
#### probetype
probetype/no.effect
#### interaction
interaction/probetype.setsize

# intrusion cost
no.effect <- lmBF(PC ~ ID, whichRandom = 'ID', data = data[data$ProbeType!='Same', ])
setsize <- lmBF(PC ~ Setsize + ID, whichRandom = 'ID', data = data[data$ProbeType!='Same', ])
probetype <- lmBF(PC ~ ProbeType + ID, whichRandom = 'ID', data = data[data$ProbeType!='Same', ])
probetype.setsize <- lmBF(PC ~ Setsize + ProbeType + ID, whichRandom = 'ID', data = data[data$ProbeType!='Same', ])
interaction <- lmBF(PC ~ Setsize*ProbeType + ID, whichRandom = 'ID', data = data[data$ProbeType!='Same', ])

#### setsize
setsize/no.effect
#### probetype
probetype/no.effect
#### interaction
interaction/probetype.setsize

# Sanity check
data$Setsize <- factor(data$Setsize)
bf = anovaBF(PC ~ Exp + ProbeType*Setsize + ID, whichRandom = 'ID', data = data)

tmp_data <- data.frame(aggregate(list(data$PC, data$RT), list(data$ProbeType, data$Setsize), mean))
tmp_data_sd <- data.frame(aggregate(list(data$PC, data$RT), list(data$ProbeType, data$Setsize), sd))
tmp_data[, 5] <- tmp_data_sd[, 3] / sqrt(20)
tmp_data[, 6] <- tmp_data_sd[, 4] / sqrt(20)
names(tmp_data) <- c('ProbeType', 'Setsize', 'PC', 'RT', 'PC_SE', 'RT_SE')
pd <- position_dodge(.1)
plot_probetype <- ggplot(data=tmp_data) + aes(x=Setsize, y = PC, linetype = ProbeType, colour = ProbeType, group = ProbeType) + 
  geom_line(position = pd, size = 1) + 
  geom_errorbar(aes(ymin=PC-PC_SE, ymax=PC+PC_SE), width=.1, position = pd, size = 1) + 
  geom_point(position = pd, size = 1) +
  # geom_line(position = pd, aes(x=Setsize, y = IM, linetype = ProbeType, group = ProbeType), color = 'red', size = 1) +
  xlab('Set Size') +
  ylab('Propotion of Correct') +
  jtools::theme_apa() +
  # scale_linetype_discrete(name = 'Probe types') +
  theme(text = element_text(size=14)) +
  theme(legend.text = element_text(size=12))  +
  theme(legend.position=c(0.3, 0.2))
# 
# pd <- position_dodge(.1)
# ggplot(data=tmp_data) + aes(x=Setsize, y = RT, linetype = ProbeType, group = ProbeType) + 
#   geom_line(position = pd, size = 1) + 
#   geom_errorbar(aes(ymin=RT-RT_SE, ymax=RT+RT_SE), width=.1, position = pd, size = 1) + 
#   geom_point(position = pd, size = 1) +
#   jtools::theme_apa() +
#   xlab('Set Size') +
#   ylab('Reaction Time (s)')

bins <- seq(0, 180, 10)
tmp_data <- data.frame()
for (sz in 1:6){
  h1 <- hist(x = exp.data[exp.data$Setsize==sz & exp.data$Response!=1,]$dissimilarity, breaks = bins, plot = 0)
  h2 <- hist(x = exp.data[exp.data$Setsize==sz,]$dissimilarity, breaks = bins, plot = 0)
  tmp_data <- rbind(tmp_data, cbind(sz, bins[-length(bins)], h1$counts/h2$counts))
}

names(tmp_data) <- c('Setsize', 'breaks', 'frequency')
tmp_data$Setsize <- factor(tmp_data$Setsize)

plot_simgradient <- ggplot(data=tmp_data)+aes(x = breaks, y = frequency, colour = Setsize, linetype = Setsize)+
  geom_line(position = pd, size = 1) +
  ylim(0, 1) +
  xlab('Similarity between target and probe') +
  ylab('Proportion of "no change" response') +
  jtools::theme_apa() +
  #geom_line(aes(breaks, IM), color = 'red', size = 2) +
  theme(text = element_text(size=14)) +
  theme(legend.position=c(0.7, 0.7))

png("Analysis/Figs/data.png", width = 800, height = 400)
plot_grid(plot_simgradient, plot_probetype, nrow=1, ncol = 2)
dev.off()


