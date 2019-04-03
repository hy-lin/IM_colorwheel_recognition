library(ggplot2)
library(BayesFactor)
library(jtools)
library(cowplot)


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
                   'IM_focus_exp', 'IM_focus_trial', 'IM_nofocus_exp', 'IM_nofocus_trial',
                   'VP_trial', 'VP_exp', 'VP_Binding_trial', 'VP_Binding_exp',
                   'SA_memory', 'SA_no_memory')
  data$ID <- factor(data$ID)
  data$TrialIndex <- factor(data$TrialIndex)
  data$TrialCondition <- factor(data$TrialCondition)
  data$Response <- factor(data$Response)
  return(data)
}

classifyProbeType <- function(data, exp, model){
  data$ProbeType <- 1
  data$dissimilarity <- 1
  for (i in 1:length(data$ProbeType)){
    if (exp == 1 | exp == 2){
      if (data$TrialCondition[i] == 'positive'){
        data$ProbeType[i] = 'positive'
        data$SimPC[i] = 1-data[i, model]
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
        data$SimPC[i] = data[i, model]
      }
      
      data$dissimilarity[i] <- wrapDistance(data$ColorProbe[i], data$ColorTarget[i])
    }
    else{
      if (data$TrialType[i] == 'recognition'){
        if (data$ColorProbe[i] == data$ColorTarget[i]){
          data$ProbeType[i] = 'Same'
          data$SimPC[i] = 1-data$IM_focus_trial[i]
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
          data$SimPC[i] = data$IM_focus_trial[i]
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

#######################

model1 = 'VP_trial'
model1_name = 'VP with knowledge of the precision of the target'
model2 = 'VP_exp'
model2_name = 'VP without the knowledge of the precision of the target'

exp2.data <- loadSimulationData(2)
exp2.data <- classifyProbeType(exp2.data, 2, model1)

exp1.data <- loadSimulationData(1)
exp1.data <- classifyProbeType(exp1.data, 1, model1)

exp.data <- rbind(exp1.data, exp2.data)
exp.data$ID <- factor(exp.data$ID)


data <- data.frame(aggregate(list(exp.data$Correctness, exp.data$RT, exp.data$SimPC), list(exp.data$ID, exp.data$ProbeType, exp.data$Setsize), mean))
names(data) <- c('ID', 'ProbeType', 'Setsize', 'PC', 'RT', 'IM')

tmp_data <- data.frame(aggregate(list(data$PC, data$RT, data$IM), list(data$ProbeType, data$Setsize), mean))
tmp_data_sd <- data.frame(aggregate(list(data$PC, data$RT), list(data$ProbeType, data$Setsize), sd))
tmp_data[, 6] <- tmp_data_sd[, 3] / sqrt(20)
tmp_data[, 7] <- tmp_data_sd[, 4] / sqrt(20)
names(tmp_data) <- c('ProbeType', 'Setsize', 'PC', 'RT', 'IM', 'PC_SE', 'RT_SE')
pd <- position_dodge(.1)
plot_probetype1 <- ggplot(data=tmp_data) + aes(x=Setsize, y = PC, linetype = ProbeType) + 
  geom_line(position = pd, size = 1) + 
  geom_errorbar(aes(ymin=PC-PC_SE, ymax=PC+PC_SE), width=.1, position = pd, size = 1) + 
  geom_point(position = pd, size = 1) +
  geom_line(position = pd, aes(x=Setsize, y = IM, linetype = ProbeType, group = ProbeType), color = 'red', size = 1) +
  xlab('Set Size') +
  ylab('Propotion of Correct') +
  jtools::theme_apa() +
  scale_linetype_discrete(name = 'Probe types') +
  theme(text = element_text(size=14)) +
  theme(legend.text = element_text(size=12))  +
  theme(legend.position=c(0.3, 0.2)) +
  ggtitle('')

bins <- seq(0, 180, 10)
tmp_data <- data.frame()
for (sz in 1:6){
  h1 <- hist(x = exp.data[exp.data$Setsize==sz & exp.data$Response!=1,]$dissimilarity, breaks = bins, plot = 0)
  h2 <- hist(x = exp.data[exp.data$Setsize==sz,]$dissimilarity, breaks = bins, plot = 0)
  tmp_data <- rbind(tmp_data, cbind(sz, bins[-length(bins)], h1$counts/h2$counts))
}
names(tmp_data) <- c('Setsize', 'breaks', 'frequency')

for (sz in 1:6){
  for (bin in bins){
    if (bin != 180){
      lower_break = bin
      higher_break = bin+10
      tmp_data$Sim[tmp_data$Setsize == sz & tmp_data$breaks == bin] <- 1-mean(exp.data[exp.data$Setsize==sz & exp.data$dissimilarity >= lower_break & exp.data$dissimilarity < higher_break, model1])
    }
  }
}

tmp_data$Setsize <- factor(tmp_data$Setsize)

plot_simgradient1 <- ggplot(data=tmp_data)+aes(x = breaks, y = frequency, linetype = Setsize)+
  geom_line(position = pd, size = 1) +
  geom_line(position = pd, aes(x=breaks, y = Sim, linetype = Setsize), color = 'red', size = 1) +
  ylim(0, 1) +
  xlab('Similarity between target and probe') +
  ylab('Proportion of "same" response') +
  jtools::theme_apa() +
  #geom_line(aes(breaks, IM), color = 'red', size = 2) +
  theme(text = element_text(size=14)) +
  theme(legend.position=c(0.7, 0.7)) +
  ggtitle(model1_name)


######################################



exp2.data <- loadSimulationData(2)
exp2.data <- classifyProbeType(exp2.data, 2, model2)

exp1.data <- loadSimulationData(1)
exp1.data <- classifyProbeType(exp1.data, 1, model2)

exp.data <- rbind(exp1.data, exp2.data)
exp.data$ID <- factor(exp.data$ID)


data <- data.frame(aggregate(list(exp.data$Correctness, exp.data$RT, exp.data$SimPC), list(exp.data$ID, exp.data$ProbeType, exp.data$Setsize), mean))
names(data) <- c('ID', 'ProbeType', 'Setsize', 'PC', 'RT', 'IM')

tmp_data <- data.frame(aggregate(list(data$PC, data$RT, data$IM), list(data$ProbeType, data$Setsize), mean))
tmp_data_sd <- data.frame(aggregate(list(data$PC, data$RT), list(data$ProbeType, data$Setsize), sd))
tmp_data[, 6] <- tmp_data_sd[, 3] / sqrt(20)
tmp_data[, 7] <- tmp_data_sd[, 4] / sqrt(20)
names(tmp_data) <- c('ProbeType', 'Setsize', 'PC', 'RT', 'IM', 'PC_SE', 'RT_SE')
pd <- position_dodge(.1)
plot_probetype2 <- ggplot(data=tmp_data) + aes(x=Setsize, y = PC, linetype = ProbeType) + 
  geom_line(position = pd, size = 1) + 
  geom_errorbar(aes(ymin=PC-PC_SE, ymax=PC+PC_SE), width=.1, position = pd, size = 1) + 
  geom_point(position = pd, size = 1) +
  geom_line(position = pd, aes(x=Setsize, y = IM, linetype = ProbeType, group = ProbeType), color = 'red', size = 1) +
  xlab('Set Size') +
  ylab('Propotion of Correct') +
  jtools::theme_apa() +
  scale_linetype_discrete(name = 'Probe types') +
  theme(text = element_text(size=14)) +
  theme(legend.text = element_text(size=12))  +
  theme(legend.position=c(0.3, 0.2)) +
  ggtitle('')

bins <- seq(0, 180, 10)
tmp_data <- data.frame()
for (sz in 1:6){
  h1 <- hist(x = exp.data[exp.data$Setsize==sz & exp.data$Response!=1,]$dissimilarity, breaks = bins, plot = 0)
  h2 <- hist(x = exp.data[exp.data$Setsize==sz,]$dissimilarity, breaks = bins, plot = 0)
  tmp_data <- rbind(tmp_data, cbind(sz, bins[-length(bins)], h1$counts/h2$counts))
}
names(tmp_data) <- c('Setsize', 'breaks', 'frequency')

for (sz in 1:6){
  for (bin in bins){
    if (bin != 180){
      lower_break = bin
      higher_break = bin+10
      tmp_data$Sim[tmp_data$Setsize == sz & tmp_data$breaks == bin] <- 1-mean(exp.data[exp.data$Setsize==sz & exp.data$dissimilarity >= lower_break & exp.data$dissimilarity < higher_break, model2])
    }
  }
}

tmp_data$Setsize <- factor(tmp_data$Setsize)

plot_simgradient2 <- ggplot(data=tmp_data)+aes(x = breaks, y = frequency, linetype = Setsize)+
  geom_line(position = pd, size = 1) +
  geom_line(position = pd, aes(x=breaks, y = Sim, linetype = Setsize), color = 'red', size = 1) +
  ylim(0, 1) +
  xlab('Similarity between target and probe') +
  ylab('Proportion of "same" response') +
  jtools::theme_apa() +
  #geom_line(aes(breaks, IM), color = 'red', size = 2) +
  theme(text = element_text(size=14)) +
  theme(legend.position=c(0.7, 0.7)) +
  ggtitle(model2_name)



png("Analysis/Figs/VPfitting.png", width = 800, height = 800)
plot_grid(plot_simgradient1, plot_probetype1, plot_simgradient2, plot_probetype2, nrow=2, ncol = 2)
dev.off()
