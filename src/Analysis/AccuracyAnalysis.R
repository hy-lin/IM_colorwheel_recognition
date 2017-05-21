library(ggplot2)

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

classifyProbeType <- function(data){
  data$ProbeType <- 1
  for (i in 1:length(data$ProbeType)){
    if (data$ColorProbe[i] == data$ColorTarget[i]){
      data$ProbeType[i] = 'Positive'
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
        data$ProbeType[i] = 'Intrusion'
      } else{
        data$ProbeType[i] = 'New'
      }
    }
    
  }
  data$ProbeType <- factor(data$ProbeType)
  return(data)
}


exp2.data <- loadData(2)
exp2.data <- classifyProbeType(exp2.data)

data <- data.frame(aggregate(list(exp2.data$Correctness, exp2.data$RT), list(exp2.data$ID, exp2.data$ProbeType, exp2.data$Setsize), mean))
names(data) <- c('ID', 'ProbeType', 'Setsize', 'PC', 'RT')

data <- data.frame(aggregate(list(data$PC, data$RT), list(data$ProbeType, data$Setsize), mean))
names(data) <- c('ProbeType', 'Setsize', 'PC', 'RT')
ggplot(data=data) + aes(x=Setsize, y = PC,linetype = ProbeType) + geom_line()
