import xmlrpc.client

def get_torrents_data(rpc_url, infohashes):
    # Initialize the ServerProxy
    # Use allow_none=True if your rTorrent config might return nulls
    proxy = xmlrpc.client.ServerProxy(rpc_url, allow_none=True)
    
    # Define the methods we want to call for each hash
    methods = ['d.name', 'd.completed_bytes', 'd.size_bytes', 'd.directory']
    
    # Build the multicall parameter list
    # Each entry is a dict with 'methodName' and 'params'
    calls = []
    for h in infohashes:
        for m in methods:
            calls.append({'methodName': m, 'params': [h]})
            
    try:
        # system.multicall takes a list of call-structs
        raw_results = proxy.system.multicall(calls)
        
        # Structure the flat results list back into a dictionary
        formatted_data = {}
        num_methods = len(methods)
        
        for i, h in enumerate(infohashes):
            # Each result from rTorrent is wrapped in a single-item list
            chunk = raw_results[i * num_methods : (i + 1) * num_methods]
            formatted_data[h] = {
                'name': chunk[0][0],
                'completed_bytes': chunk[1][0],
                'size_bytes': chunk[2][0],
                'directory': chunk[3][0]
            }
        return formatted_data

    except xmlrpc.client.Fault as e:
        print(f"A fault occurred: {e.faultString}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example Usage
rpc_link = "http://localhost:81/RPC2"
my_hashes = ["916F5AEE966E545F2A60F3327B0578B9BAF14352", "44BB6FAA1F14F8A6F04EC6CAB304D1461EA75D59"]
data = get_torrents_data(rpc_link, my_hashes)

for h, stats in data.items():
    print(f"Torrent {h}: {stats['name']} ({stats['completed_bytes']}/{stats['size_bytes']} bytes)")
