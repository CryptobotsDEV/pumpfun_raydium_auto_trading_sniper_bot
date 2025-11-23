#!/usr/bin/env python3
"""
==============================================================================
🚀 CRYPTOBOTS.DEV - SNIPER TRADING BOT v3.3a - DEMO VERSION 🚀
==============================================================================

⚠️  DEMONSTRATION VERSION - This shows the exact structure and functionality 
    of the real CryptoBots Sniper Bot, but uses simulated data instead 
    of making actual API calls or blockchain transactions.

🔥 GET FULL VERSION: https://cryptobots.dev (Starting at $0)
💬 TELEGRAM SUPPORT: https://t.me/cryptobots_dev

FULL VERSION FEATURES:
🎯 Multi-exchange sniping (Raydium, PumpFun, DexScreener)
💹 Real-time position monitoring with live ROI tracking
🛡️ Advanced token safety filters and rug detection
⚡ Lightning-fast execution with MEV protection
📊 Comprehensive analytics and P&L tracking
🤖 Telegram bot integration for remote control
💎 Multiple take-profit levels with trailing stops
🔄 Automated position management and cleanup

This demo replicates the EXACT interface and workflow but with fake data.
==============================================================================
"""

import json
import time
import random
import threading
import os
import sys
import signal
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Dict, List, Optional

# COLOR SETUP - EXACTLY LIKE ORIGINAL
os.system("color")
green = '\033[32m'
red = '\033[31m' 
yellow = '\033[33m'
cyan = '\033[96m'
pink = '\033[95m'
gray = '\033[90m'
white = '\033[97m'
reset = '\033[0m'

# DEMO CONSTANTS
app_name = "sniper_demo"
sniper_version = "v3.3a-DEMO"
FREE_VERSION = True
SIM_MODE = True

# SIMULATED SETTINGS
wallet_address = "DemoWallet1234567890abcdefghijklmnopqr"
sol_buy_amount = 0.01
starting_bal = 5.0
bot_bal = starting_bal
max_positions = 3
pos_max_runtime = 15.0
report_interval = 0.5
sol_price = 248.75
slippage = 5

# DEMO DATA
SAMPLE_TOKENS = [
    {"mint": "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM", "symbol": "PEPE", "name": "Pepe Token", "market": "PumpFun"},
    {"mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v", "symbol": "DOGE", "name": "Dogecoin Token", "market": "Raydium"},
    {"mint": "J1toso1uCk3RLmjorhTtrVwY9HJ7X8V9yYac6Y7kGCPn", "symbol": "BONK", "name": "Bonk Token", "market": "DexScreener"},
    {"mint": "mSoLzYCxHdYgdzU16g5QSh3i5K3z3KZK7ytfqcJm7So", "symbol": "mSOL", "name": "Marinade SOL", "market": "Raydium"},
    {"mint": "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263", "symbol": "SAMO", "name": "Samoyedcoin", "market": "PumpFun"}
]

# GLOBAL STATE
active_positions = 0
open_positions = {}
position_threads = []
total_mints_detected = 0
profitable_trades = 0
loss_trades = 0
total_trades = 0
total_events_checked = 0
queue_size = 0
start_time = time.time()
last_report_time = time.time()
stop_event = threading.Event()

@dataclass
class Position:
    """Demo position data structure"""
    mint: str
    symbol: str
    name: str
    market: str
    entry_price: float
    entry_time: float
    tokens_bought: float
    sol_spent: float
    current_price: float
    current_roi: float
    status: str = "ACTIVE"
    exit_time: Optional[float] = None
    exit_price: Optional[float] = None
    profit_loss: Optional[float] = None

class CryptobotsSniperDemo:
    """
    Demo version of CryptoBots Sniper Bot with simulated operations
    """
    
    def __init__(self):
        self.positions: Dict[str, Position] = {}
        self.session_start = time.time()
        
    def print_banner(self):
        """Print the exact ASCII banner from original"""
        print(f"""{green}
███████╗███╗   ██╗ ██╗██████╗ ███████╗██████╗     ████████╗██████╗  █████╗ ██████╗ ██╗███╗   ██╗ ██████╗     ██████╗  ██████╗ ████████╗
██╔════╝████╗  ██║ ██║██╔══██╗██╔════╝██╔══██╗    ╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██║████╗  ██║██╔════╝     ██╔══██╗██╔═══██╗╚══██╔══╝
███████╗██╔██╗ ██║ ██║██████╔╝█████╗  ██████╔╝       ██║   ██████╔╝███████║██║  ██║██║██╔██╗ ██║██║  ███╗    ██████╔╝██║   ██║   ██║   
╚════██║██║╚██╗██║ ██║██╔═══╝ ██╔══╝  ██╔══██╗       ██║   ██╔══██╗██╔══██║██║  ██║██║██║╚██╗██║██║   ██║    ██╔══██╗██║   ██║   ██║   
███████║██║ ╚████║ ██║██║     ███████╗██║  ██║       ██║   ██║  ██║██║  ██║██████╔╝██║██║ ╚████║╚██████╔╝    ██████╔╝╚██████╔╝   ██║   
╚══════╝╚═╝  ╚═══╝ ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝       ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝╚═╝  ╚═══╝ ╚═════╝     ╚═════╝  ╚═════╝    ╚═╝   
          [ https://t.me/cryptobots_dev ] [ https://t.me/rikardionsdev ] [ https://cryptobots.dev ] [ @cryptobots_dev ]
          {reset}""")

    def print_config_summary(self):
        """Print configuration summary exactly like original"""
        def print_section_header(title):
            print(f"\n{green}══════════ {title.upper()} ══════════{reset}")
        
        print(f"✅ CONFIGURATION LOADED SUCCESSFULLY")
        print(f"{gray}   Demo Config v3.3a, Simulated Settings'\n{'_' * 120}{reset}")
        
        print_section_header("Enabled Sniper Modes")
        print("RAYDIUM | PUMPFUN | DEXSCREENER")
        
        print_section_header("Enabled Mode Settings")
        print("SCAN_V4         SCAN_CPMM       SCAN_CLMM")
        print("PF_MINTS        PF_TRADES       SIM_MODE")
        print("SAVE_LOGS       TRACK_MINTS     MULTI_TP")
        
        print_section_header("Active Buy Settings")
        print(f"  {gray}• Buy Amount per Token: {sol_buy_amount} SOL (${sol_buy_amount * sol_price:.2f}){reset}")
        print(f"  {gray}• Max Open Positions: {max_positions}{reset}")
        print(f"  {gray}• Position Max Runtime: {pos_max_runtime} minutes{reset}")
        print(f"  {gray}• Default Slippage: {slippage}%{reset}")
        
        print_section_header("Active Sell Settings")
        print(f"  {gray}• Take Profit 1: 50% at +25% ROI{reset}")
        print(f"  {gray}• Take Profit 2: 25% at +50% ROI{reset}")
        print(f"  {gray}• Take Profit 3: 25% at +100% ROI{reset}")
        print(f"  {gray}• Stop Loss: -20% ROI{reset}")
        print(f"  {gray}• Max Position Time: {pos_max_runtime} min{reset}")
        
        print_section_header("Token Safety Settings")
        print(f"  {gray}• Min SOL Liquidity: 0.005 SOL{reset}")
        print(f"  {gray}• Max Market Cap: $10,000,000{reset}")
        print(f"  {gray}• Max Risk Score: 40000{reset}")
        print(f"  {gray}• Max Bundled Wallets: 5{reset}")

    def simulate_token_detection(self) -> Optional[dict]:
        """Simulate token detection from various sources"""
        global total_events_checked, queue_size
        
        total_events_checked += random.randint(5, 15)
        queue_size = random.randint(0, 25)
        
        if random.random() < 0.4:  # 40% chance of finding a token (increased for more action)
            token = random.choice(SAMPLE_TOKENS)
            return {
                "mint": token["mint"],
                "symbol": token["symbol"], 
                "name": token["name"],
                "market": token["market"],
                "pool_type": random.choice(["RAYDIUM_V4", "PUMPFUN", "RAYDIUM_CPMM"]),
                "signature": f"{''.join(random.choices('0123456789abcdef', k=88))}",
                "liquidity": random.uniform(5.0, 100.0),
                "market_cap": random.uniform(50000, 2000000),
                "price": random.uniform(0.00001, 0.005)
            }
        return None

    def create_position(self, token_data: dict) -> bool:
        """Simulate creating a new trading position"""
        global active_positions, open_positions, total_mints_detected
        
        if active_positions >= max_positions:
            print(f"\t{gray}Max positions reached, skipping {token_data['symbol']}...{reset}")
            return False
            
        # Simulate buy execution
        entry_price = token_data["price"] * (1 + random.uniform(-0.02, 0.02))  # Small price variation
        tokens_bought = sol_buy_amount / entry_price
        
        position = Position(
            mint=token_data["mint"],
            symbol=token_data["symbol"],
            name=token_data["name"],
            market=token_data["market"],
            entry_price=entry_price,
            entry_time=time.time(),
            tokens_bought=tokens_bought,
            sol_spent=sol_buy_amount,
            current_price=entry_price,
            current_roi=0.0
        )
        
        self.positions[token_data["mint"]] = position
        open_positions[token_data["mint"]] = position.symbol
        active_positions += 1
        total_mints_detected += 1
        
        # Original format buy message
        tp_message = f"\t{gray}• Take Profits: TP1(25%) TP2(50%) TP3(100%) | Stop Loss: -20%{reset}"
        print(f"\n🟢 BUYING: https://dexscreener.com/solana/{token_data['mint']}?maker={wallet_address}\n\n{tp_message}")
        
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"\t✅ {green}BUY [SUCCESS] for {token_data['mint']} - {token_data['pool_type']} - {current_time}{reset}")
        
        # Start monitoring thread
        monitor_thread = threading.Thread(
            target=self.monitor_position, 
            args=(token_data["mint"],), 
            daemon=True
        )
        monitor_thread.start()
        position_threads.append(monitor_thread)
        
        return True

    def monitor_position(self, mint: str):
        """Monitor a position with live price updates and ROI calculation"""
        global active_positions, profitable_trades, loss_trades, total_trades, bot_bal
        
        position = self.positions.get(mint)
        if not position:
            return
            
        start_time = time.time()
        # Make it more profitable - 70% pump, 20% volatile, 10% sideways
        price_trend = random.choices(["pump", "volatile", "sideways"], weights=[70, 20, 10])[0]
                
        while not stop_event.is_set() and position.status == "ACTIVE":
            runtime = (time.time() - start_time) / 60  # minutes
            
            # Simulate price movement based on trend (more profitable)
            if price_trend == "pump":
                price_change = random.uniform(-0.01, 0.12)  # Strong upward bias
            elif price_trend == "volatile":
                price_change = random.uniform(-0.08, 0.15)  # High volatility with upward bias
            else:  # sideways
                price_change = random.uniform(-0.01, 0.03)  # Slight upward bias
                
            position.current_price *= (1 + price_change)
            position.current_roi = ((position.current_price - position.entry_price) / position.entry_price) * 100
            
            # Check exit conditions
            should_exit = False
            exit_reason = ""
            
            # Take profit conditions
            if position.current_roi >= 100:  # 100% profit
                should_exit = True
                exit_reason = "TP3 (+100%)"
            elif position.current_roi >= 50:  # 50% profit
                should_exit = True
                exit_reason = "TP2 (+50%)"
            elif position.current_roi >= 25:  # 25% profit
                should_exit = True
                exit_reason = "TP1 (+25%)"
            # Stop loss
            elif position.current_roi <= -20:
                should_exit = True
                exit_reason = "STOP LOSS (-20%)"
            # Max runtime
            elif runtime >= pos_max_runtime:
                should_exit = True
                exit_reason = f"MAX TIME ({pos_max_runtime}min)"
            
            if should_exit:
                self.close_position(mint, exit_reason)
                break
                
            # Show periodic updates in original format
            roi_color = green if position.current_roi >= 0 else red
            time_remaining = max(0, pos_max_runtime - runtime)
            time_str = f"{time_remaining:.1f}min"
            roi_str = f"ROI: {roi_color}{position.current_roi:+.2f}%{reset}"
            pf_bond_progress = min(100, (runtime / pos_max_runtime) * 100)
            
            # Determine next TP target
            if position.current_roi < 25:
                next_roi = 25.0
                current_tp_index = 0
            elif position.current_roi < 50:
                next_roi = 50.0
                current_tp_index = 1
            elif position.current_roi < 100:
                next_roi = 100.0
                current_tp_index = 2
            else:
                next_roi = 100.0
                current_tp_index = 2
            
            print(f'{pink}Target TP{current_tp_index + 1}/3 [{reset} {roi_color}{position.current_roi:>6.2f}{reset}{pink} /{reset} {green}{next_roi:>6.1f}%{reset} {pink}] for [{position.mint:<44}] [Remaining {time_str:>8}] {roi_str} [Bonding {pf_bond_progress:>5.2f}%] [{position.symbol}]{reset}')
            
            time.sleep(2)  # Update every 2 seconds

    def close_position(self, mint: str, reason: str):
        """Close a position and calculate P&L"""
        global active_positions, profitable_trades, loss_trades, total_trades, bot_bal
        
        position = self.positions.get(mint)
        if not position or position.status != "ACTIVE":
            return
            
        position.status = "CLOSED"
        position.exit_time = time.time()
        position.exit_price = position.current_price
        
        # Calculate profit/loss
        sol_received = position.tokens_bought * position.current_price
        position.profit_loss = sol_received - position.sol_spent
        
        # Update global stats
        active_positions -= 1
        total_trades += 1
        
        if position.profit_loss > 0:
            profitable_trades += 1
            bot_bal += position.profit_loss
            result_color = green
            result_emoji = "✅"
        else:
            loss_trades += 1
            bot_bal += position.profit_loss  # This will be negative
            result_color = red  
            result_emoji = "❌"
            
        # Remove from open positions
        if mint in open_positions:
            del open_positions[mint]
            
        runtime = (position.exit_time - position.entry_time) / 60
        
        # Original format sell messages
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if "TP" in reason:
            tp_num = reason.split("(")[0].replace("TP", "").strip()
            tp_percent = reason.split("(")[1].replace(")", "").replace("%", "") if "(" in reason else "25"
            display_sell_percentage = 100.0  # Selling 100% for demo
            
            print(f'\n⚠️ {green} SELLING {display_sell_percentage:.2f}% at TP{tp_num}/3 (TP{tp_num}: {tp_percent}%) [{position.symbol}] with approx ROI: {position.current_roi:.2f}%{reset}')
            print(f'{gray}https://dexscreener.com/solana/{position.mint}?maker={wallet_address}{reset}\n')
            print(f"\t✅ {green}SELL [SUCCESS] {display_sell_percentage:.2f}% at TP{tp_num}/3 (TP{tp_num}: {tp_percent}%) with approx ROI: {position.current_roi:.2f}% [{position.mint}] - {current_time}{reset}")
        else:
            print(f"{result_emoji} CLOSED {position.symbol}: {reason} | ROI: {result_color}{position.current_roi:+.1f}%{reset} | P&L: {result_color}{position.profit_loss:+.4f} SOL{reset} | Time: {runtime:.1f}min")
            print(f"\t{gray}> Cryptobots.DEV Sniper closed position successfully! [{mint[:8]}...]{reset}")

    def show_status_report(self):
        """Show periodic status report in original compact format"""
        global last_report_time, total_events_checked, queue_size
        
        current_time = time.time()
        if current_time - last_report_time < 8:  # Every 8 seconds
            return
            
        last_report_time = current_time
        runtime = time.time() - start_time
        runtime_formatted = str(timedelta(seconds=int(runtime)))
        win_rate = (profitable_trades / total_trades * 100) if total_trades > 0 else 0
        
        # Calculate TPS
        transactions_per_second = total_events_checked / runtime if runtime > 0 else 0
        
        # Queue color based on size
        if queue_size <= 5:
            ev_color = green
        elif queue_size <= 15:
            ev_color = yellow
        else:
            ev_color = red
            
        # P&L calculation
        pnl = bot_bal - starting_bal
        if pnl >= 0:
            pnl_message = f"{green}+{pnl:.5f} SOL{reset}"
        else:
            pnl_message = f"{red}{pnl:.5f} SOL{reset}"
            
        # SOL price color (simulate price movement)
        sol_price_color = random.choice([green, red])
        
        # Original compact format
        print(f"{gray}- Tx: {total_events_checked} [{reset}{ev_color}{queue_size}{reset}{gray}] | TPS: {transactions_per_second:.2f} | Open: {active_positions}/{max_positions} | Runtime: {runtime_formatted} | Tokens Checked: {total_mints_detected} | P({profitable_trades}) L({loss_trades}) T({total_trades}) | Bot Balance: {bot_bal:.5f} SOL | PnL: {pnl:.5f} SOL ({reset}{pnl_message}{gray}) |{reset}{sol_price_color} SOL ${sol_price:.2f} {reset}{gray}| Winrate: {win_rate:.2f} % {reset}")

    def handle_exit(self):
        """Handle CTRL+C exit with summary like original"""
        global stop_event
        
        print(f"\n{yellow}🛑 STOP signal received (CTRL+C)! Closing all positions...{reset}")
        stop_event.set()
        
        # Close all active positions
        for mint, position in list(self.positions.items()):
            if position.status == "ACTIVE":
                self.close_position(mint, "MANUAL STOP")
        
        # Wait for all threads to finish
        for thread in position_threads:
            if thread.is_alive():
                thread.join(timeout=5)
        
        time.sleep(2)  # Give time for final updates
        
        self.show_exit_summary()

    def show_exit_summary(self):
        """Show exit summary with ASCII banner like original"""
        global bot_bal, starting_bal, profitable_trades, loss_trades, total_trades, total_mints_detected
        
        runtime = time.time() - start_time
        runtime_formatted = str(timedelta(seconds=int(runtime)))
        win_rate = (profitable_trades / total_trades * 100) if total_trades > 0 else 0
        bal_change = bot_bal - starting_bal
        bal_change_pct = (bal_change / starting_bal * 100) if starting_bal > 0 else 0
        bal_color = green if bal_change >= 0 else red
        
        print(f'\n{bal_color}Final SOL Balance: {bot_bal:.4f} SOL [Changed by {bal_change_pct:.3f}% that is {bal_change:.5f} SOL ]{reset}')
        print(f'Total Runtime: {runtime_formatted}, Total Tokens Considered for Buying [{total_mints_detected}]\nProfitable Trades [{profitable_trades}], Trades with Loss [{loss_trades}], Total Trades across all TPs [{total_trades}]\n')
        
        print(f"\n✅ Completed!")
        print(f"{gray}{'_' * 134}{reset}\n")
        print(f"""{green}
███████╗███╗   ██╗ ██╗██████╗ ███████╗██████╗     ████████╗██████╗  █████╗ ██████╗ ██╗███╗   ██╗ ██████╗     ██████╗  ██████╗ ████████╗
██╔════╝████╗  ██║ ██║██╔══██╗██╔════╝██╔══██╗    ╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██║████╗  ██║██╔════╝     ██╔══██╗██╔═══██╗╚══██╔══╝
███████╗██╔██╗ ██║ ██║██████╔╝█████╗  ██████╔╝       ██║   ██████╔╝███████║██║  ██║██║██╔██╗ ██║██║  ███╗    ██████╔╝██║   ██║   ██║   
╚════██║██║╚██╗██║ ██║██╔═══╝ ██╔══╝  ██╔══██╗       ║   ██╔══██╗██╔══██║██║  ██║██║██║╚██╗██║██║   ██║    ██╔══██╗██║   ██║   ██║   
███████║██║ ╚████║ ██║██║     ███████╗██║  ██║       ██║   ██║  ██║██║  ██║██████╔╝██║██║ ╚████║╚██████╔╝    ██████╔╝╚██████╔╝   ██║   
╚══════╝╚═╝  ╚═══╝ ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝       ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝╚═╝  ╚═══╝ ╚═════╝     ╚═════╝  ╚═════╝    ╚═╝   
          [ https://t.me/cryptobots_dev ] [ https://t.me/rikardionsdev ] [ https://cryptobots.dev ] [ @cryptobots_dev ]
          {reset}""")
        print(f"{gray}{'_' * 134}{reset}")

    def run_trading_loop(self):
        """Main trading loop - token detection and position management"""
        print(f"\n{green}🚀 SNIPER BOT STARTED - SEARCHING FOR OPPORTUNITIES...{reset}")
        print(f"{yellow}Press CTRL+C to stop gracefully and see summary{reset}\n")
        
        try:
            while not stop_event.is_set():
                # Simulate token detection
                token_data = self.simulate_token_detection()
                
                if token_data:
                    # Show detection message for ALL tokens (both accepted and rejected)
                    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(f"{gray} {'-'*120} {reset}\n🚀 {green}NEW {token_data['pool_type']} Token Detected at {current_time}, analyzing ... {reset}\n\t{gray}https://solscan.io/tx/{token_data['signature']}\n {'-'*120} {reset}")
                    
                    # Simulate safety checks with higher pass rate for profitability
                    if random.random() > 0.2:  # 80% pass safety checks
                        self.create_position(token_data)
                    else:
                        print(f"\t{red}❌ REJECTED: Failed safety checks - skipping{reset}")
                
                # Show periodic status reports
                self.show_status_report()
                
                # Shorter, more consistent delay to prevent pauses
                time.sleep(random.uniform(2, 5))
                
        except KeyboardInterrupt:
            self.handle_exit()

    def run(self):
        """Main entry point"""
        # Show banner and config
        self.print_banner()
        print(f"{cyan}════════════════════════════════════════════════════════════════════════════════")
        print(f"                   {green}CRYPTOBOTS.DEV - SNIPER TRADING BOT v3.3a DEMO{cyan}")
        print(f"                       {yellow}Professional Multi-Exchange Sniping{cyan}")
        print(f"═════════════════════════════════════════════════════════════════════════════════{reset}")
        
        print(f"\n{yellow}💎 FREE DEMO VERSION:{reset}")
        print(f"   {gray}• Shows exact interface and functionality of full version{reset}")
        print(f"   {gray}• All trades are simulated (no real trading){reset}")
        print(f"   {gray}• Perfect for testing strategies and learning the system{reset}")
        
        print(f"\n{green}🚀 FULL VERSION FEATURES:{reset}")
        print(f"   {gray}• Real multi-exchange sniping (Raydium, PumpFun, DexScreener){reset}")
        print(f"   {gray}• Lightning-fast execution with MEV protection{reset}")
        print(f"   {gray}• Advanced safety filters and rug detection{reset}")
        print(f"   {gray}• Live position monitoring with ROI tracking{reset}")
        print(f"   {gray}• Telegram bot integration for remote control{reset}")
        print(f"   {gray}• Comprehensive analytics and reporting{reset}")
        
        print(f"\n{cyan}🔗 Get Full Version: {white}https://cryptobots.dev{reset} {yellow}(Starting at $0){reset}")
        print(f"{cyan}💬 Support & Updates: {white}https://t.me/cryptobots_dev{reset}")
        
        self.print_config_summary()
        
        print(f"{gray}{'_' * 123}{reset}")
        print(f"\n{red}>{reset} Your SNIPER bot {red}{wallet_address}{reset} is ready for trading with {red}{sol_buy_amount} SOL{reset} (${(sol_price * sol_buy_amount):.2f}) per token")
        print(f'\n{red}>{reset} When you want to STOP THE BOT, press {red}CTRL+C{reset} to SELL ALL and EXIT, dont force close the bot or positions will stay open')
        
        input(f'\n{red}>{reset} Press {red}ENTER{reset} to connect and wait for trades\n')
        
        # Check balance simulation
        print(f"[ {green}SNIPER TRADING bot SOL balance enough: {starting_bal:.3f} SOL (${(sol_price*starting_bal):.2f}), min for your settings: {(sol_buy_amount*max_positions):.3f} SOL{reset} ]")
        
        # Start trading loop
        self.run_trading_loop()

if __name__ == "__main__":
    def signal_handler(signum, frame):
        """Handle CTRL+C gracefully"""
        demo.handle_exit()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        demo = CryptobotsSniperDemo()
        demo.run()
    except KeyboardInterrupt:
        print(f"\n\n{yellow}Program interrupted by user. Goodbye!{reset}")
    except Exception as e:
        print(f"\n{red}❌ An error occurred: {str(e)}{reset}")
        print(f"{cyan}💬 Report issues at: {white}https://t.me/cryptobots_dev{reset}")
