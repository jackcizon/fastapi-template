-- KEYS[1]: Ratelimit Key
-- ARGV[1]: Capacity
-- ARGV[2]: Rate per second
-- ARGV[3]: Current Timestamp
-- ARGV[4]: request token count, typically 1

local bucket_info = redis.call('HMGET', KEYS[1], 'tokens', 'last_time')
local tokens = tonumber(bucket_info[1])
local last_time = tonumber(bucket_info[2])

if tokens == nil then
	tokens = tonumber(ARGV[1])
	last_time = tonumber(ARGV[3])
end

local now = tonumber(ARGV[3])
local delta_time = math.max(0, now - last_time)
local new_tokens = delta_time * tonumber(ARGV[2])
local current_tokens = math.min(tonumber(ARGV[1]), tokens + new_tokens)

local allowed = 0
if current_tokens >= tonumber(ARGV[4]) then
	current_tokens = current_tokens - ARGV[4]
	allowed = 1
end

redis.call('HMSET', KEYS[1], 'tokens', current_tokens, 'last_time', now)
redis.call('EXPIRE', KEYS[1], math.ceil(ARGV[1] / ARGV[2]) * 2)
return allowed