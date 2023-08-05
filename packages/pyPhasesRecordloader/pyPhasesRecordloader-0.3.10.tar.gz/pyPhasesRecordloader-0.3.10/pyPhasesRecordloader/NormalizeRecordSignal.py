from pyPhases.util.Logger import classLogger
from pyPhasesRecordloader.RecordSignal import RecordSignal
from pyPhasesRecordloader.Signal import Signal


@classLogger
class NormalizeRecordSignal:
    def combine(self, signal: RecordSignal, combineChannels):
        from pyPhasesRecordloader.RecordLoader import ChannelsNotPresent

        for combineConfig in combineChannels:
            newChannelName = combineConfig["name"]
            channelType = combineConfig["type"]
            channels = combineConfig["channel"]
            if newChannelName in signal.signalNames and "overwrite" not in combineConfig:
                self.logError("Channel %s already exists" % newChannelName)
                continue

            if newChannelName in signal.signalNames and not combineConfig["overwrite"]:
                continue

            type = combineConfig["combineType"]

            if type == "mean":
                signal.combine(channels, newChannelName)
            elif type == "derived":
                signal.derive(channels, newChannelName)
            elif type == "copy":
                srcSignal = signal.getSignalByName(channels)
                srcArray = srcSignal.signal.copy()
                s = Signal(newChannelName, srcArray, srcSignal.frequency)
                signal.addSignal(s)
            elif type == "select":
                found = False
                for name in channels:
                    if name in signal.signalNames:
                        index = signal.getSignalIndexByName(name)
                        signal.signals[index].name = newChannelName
                        signal.signalNames[index] = newChannelName
                        found = True
                        break
                if not found:
                    self.logError("Missing channel %s for %s" % (newChannelName, signal.recordId))
                    raise ChannelsNotPresent(channels, signal.recordId)
            elif type == "selectByQuality":
                bestChannelIndex = -1
                bestQuality = -1
                for name in channels:
                    if name in signal.signalNames:
                        index = signal.getSignalIndexByName(name)
                        quality = signal.signals[index].quality
                        if quality is not None and quality > bestQuality:
                            bestQuality = quality
                            bestChannelIndex = index
                if bestChannelIndex >= 0:
                    signal.signals[bestChannelIndex].name = newChannelName
                    signal.signalNames[bestChannelIndex] = newChannelName
                else:
                    self.logError(
                        "Missing channel %s for %s or missing signal quality for channel selection"
                        % (newChannelName, signal.recordId)
                    )
                    raise ChannelsNotPresent(channels, signal.recordId)
            else:
                raise Exception("Combine type %s does not exist" % type)

            newSignal = signal.getSignalByName(newChannelName)
            newSignal.typeStr = channelType
            newSignal.setSignalTypeFromTypeStr()
