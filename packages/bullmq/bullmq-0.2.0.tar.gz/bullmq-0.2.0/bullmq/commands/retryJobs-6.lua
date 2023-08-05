--[[
  Attempts to retry all failed jobs
  Input:
    KEYS[1] base key
    KEYS[2] events stream
    KEYS[3] state key (failed, completed)
    KEYS[4] 'wait'
    KEYS[5] 'paused'
    KEYS[6] 'meta'
    ARGV[1] count
    ARGV[2] timestamp
    ARGV[3] prev state
  Output:
    1  means the operation is not completed
    0  means the operation is completed
]]
local maxCount = tonumber(ARGV[1])
local timestamp = tonumber(ARGV[2])
local rcall = redis.call;
-- Includes
--[[
  Function to loop in batches.
  Just a bit of warning, some commands as ZREM
  could receive a maximum of 7000 parameters per call.
]]
local function batches(n, batchSize)
  local i = 0
  return function()
    local from = i * batchSize + 1
    i = i + 1
    if (from <= n) then
      local to = math.min(from + batchSize - 1, n)
      return from, to
    end
  end
end
--[[
  Function to check for the meta.paused key to decide if we are paused or not
  (since an empty list and !EXISTS are not really the same).
]]
local function getTargetQueueList(queueMetaKey, waitKey, pausedKey)
  if rcall("HEXISTS", queueMetaKey, "paused") ~= 1 then
    return waitKey
  else
    return pausedKey
  end
end
local target = getTargetQueueList(KEYS[6], KEYS[4], KEYS[5])
local jobs = rcall('ZRANGEBYSCORE', KEYS[3], 0, timestamp, 'LIMIT', 0, maxCount)
if (#jobs > 0) then
  for i, key in ipairs(jobs) do
    local jobKey = KEYS[1] .. key
    rcall("HDEL", jobKey, "finishedOn", "processedOn", "failedReason", "returnvalue")
    -- Emit waiting event
    rcall("XADD", KEYS[2], "*", "event", "waiting", "jobId", key, "prev", ARGV[3]);
  end
  for from, to in batches(#jobs, 7000) do
    rcall("ZREM", KEYS[3], unpack(jobs, from, to))
    rcall("LPUSH", target, unpack(jobs, from, to))
  end
end
maxCount = maxCount - #jobs
if(maxCount <= 0) then
  return 1
end
return 0
