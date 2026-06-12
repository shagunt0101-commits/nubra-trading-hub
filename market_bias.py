def market_bias(board):
    """Analyze market bias using OI-weighted analysis of option chains"""
    
    # Filter for ATM and near-ATM strikes only (more relevant for bias)
    if board.empty or 'oi' not in board.columns:
        return "NEUTRAL"
    
    try:
        # Separate CE and PE
        ce_board = board[board["type"] == "CE"]
        pe_board = board[board["type"] == "PE"]
        
        if ce_board.empty or pe_board.empty:
            return "NEUTRAL"
        
        # Calculate total OI for calls and puts
        total_ce_oi = ce_board["oi"].sum()
        total_pe_oi = pe_board["oi"].sum()
        
        if total_ce_oi == 0 and total_pe_oi == 0:
            return "NEUTRAL"
        
        # PCR (Put-Call Ratio) analysis
        pcr = total_pe_oi / total_ce_oi if total_ce_oi > 0 else 0
        
        # Bias determination based on PCR
        # High PCR (>1.2) = More puts = Defensive = BEARISH
        # Low PCR (<0.8) = More calls = Aggressive = BULLISH  
        # 0.8-1.2 = Balanced = NEUTRAL
        
        if pcr > 1.2:
            return "BEARISH"
        elif pcr < 0.8:
            return "BULLISH"
        else:
            return "NEUTRAL"
            
    except Exception as e:
        print(f"Error in market_bias: {e}")
        return "NEUTRAL"
