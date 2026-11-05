"""Fixed prices from the Module 1 lab (USD / 1M tokens)."""
PRICES={"uncached_input":2.00,"cache_write":2.50,"cached_input":0.20,"output":10.00}
def price(uncached_input,cache_write,cached_input,output):
    return sum((uncached_input*2.0,cache_write*2.5,cached_input*0.2,output*10.0))/1e6
def loop(turns,initial_file_tokens=0):
    inp=sum(8000+(i-1)*1500+initial_file_tokens for i in range(1,turns+1))
    out=turns*400
    return {"turns":turns,"input":inp,"output":out,"total_usd":price(inp,0,0,out)}
def tickets(cost_per_attempt,success,count=1000,human_cost=2):
    attempts=count*(2-success)
    people=count*(1-success)**2
    api=attempts*cost_per_attempt
    return {"attempts":attempts,"api_usd":api,"human_tickets":people,"human_usd":people*human_cost,"total_usd":api+people*human_cost}
