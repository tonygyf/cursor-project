"""
@description 拔钉子游戏核心逻辑
@author Your Name
@date 2024
"""

from level_configs import LEVELS, NailType

class Nail:
    def __init__(self, id, x, y, nail_type):
        """
        @param id: 钉子编号
        @param x: x坐标
        @param y: y坐标
        @param nail_type: 钉子类型
        """
        self.id = id
        self.x = x
        self.y = y
        self.nail_type = nail_type
        self.is_removed = False
        self.dependencies = []

class NailStack:
    def __init__(self, max_size):
        """
        @param max_size: 栈的最大容量
        """
        self.max_size = max_size
        self.items = []
        self.current_type = None

    def can_push(self, nail):
        """
        检查是否可以将钉子压入栈
        """
        if len(self.items) >= self.max_size:
            return False
        if not self.items:
            return True
        return nail.nail_type == self.current_type

    def push(self, nail):
        """
        压入钉子
        """
        if not self.can_push(nail):
            return False
        self.items.append(nail)
        self.current_type = nail.nail_type
        if len(self.items) >= self.max_size:
            self.clear()
        return True

    def clear(self):
        """
        清空栈
        """
        self.items = []
        self.current_type = None

class NailGame:
    def __init__(self, level_num=1):
        """
        @param level_num: 当前关卡编号
        """
        if level_num not in LEVELS:
            raise ValueError(f"关卡{level_num}不存在!")
        
        self.current_player = 1
        self.level_config = LEVELS[level_num]
        self.nails = {}
        self.stacks = [NailStack(self.level_config.stack_size)]
        self.game_over = False
        self._initialize_level()

    def _initialize_level(self):
        """
        初始化关卡
        """
        for nail_id, pos in self.level_config.nail_positions.items():
            self.nails[nail_id] = Nail(
                nail_id, 
                pos[0], 
                pos[1], 
                self.level_config.nail_types[nail_id]
            )
        
        for nail_id, deps in self.level_config.dependencies.items():
            self.nails[nail_id].dependencies = [self.nails[dep_id] for dep_id in deps]

    def can_remove(self, nail_id):
        """
        检查是否可以拔出钉子
        """
        if nail_id not in self.nails:
            return False
        
        nail = self.nails[nail_id]
        if nail.is_removed:
            return False
            
        return all(dep.is_removed for dep in nail.dependencies)

    def remove_nail(self, nail_id):
        """
        尝试拔出钉子
        """
        if not self.can_remove(nail_id):
            return False
        
        nail = self.nails[nail_id]
        nail.is_removed = True
        
        # 尝试将钉子放入任何一个可用的栈中
        for stack in self.stacks:
            if stack.can_push(nail):
                stack.push(nail)
                self.current_player = 3 - self.current_player
                return True
        
        # 如果所有栈都无法放入，游戏结束
        self.game_over = True
        return False

    def add_stack(self):
        """
        添加新的栈
        """
        self.stacks.append(NailStack(self.level_config.stack_size))

    def is_level_complete(self):
        """
        检查关卡是否完成
        """
        return all(nail.is_removed for nail in self.nails.values())

    def display_nails(self):
        """
        显示当前关卡状态
        """
        print(f"\n=== {self.level_config.description} ===")
        
        # 创建显示网格
        grid = [[' ' for _ in range(self.level_config.width)] for _ in range(self.level_config.height)]
        
        # 放置钉子
        for nail in self.nails.values():
            grid[nail.y][nail.x] = '○' if nail.is_removed else '●'
        
        # 显示网格
        for row in grid:
            print('  ' + ' '.join(row))
        
        # 显示依赖关系
        print("\n钉子依赖关系:")
        for nail in self.nails.values():
            if nail.dependencies:
                deps = [str(dep.id) for dep in nail.dependencies]
                print(f"钉子{nail.id}依赖于: 钉子{', '.join(deps)}")
        
        # 显示可拔出的钉子
        print("\n可拔出的钉子:", end=" ")
        available = [str(nail_id) for nail_id, nail in self.nails.items() 
                    if not nail.is_removed and self.can_remove(nail_id)]
        print("钉子" + ", 钉子".join(available) if available else "无")
        
        print("已拔出的钉子:", end=" ")
        removed = [str(nail_id) for nail_id, nail in self.nails.items() 
                  if nail.is_removed]
        print("钉子" + ", 钉子".join(removed) if removed else "无")
        print()

def main():
    current_level = 1
    max_level = len(LEVELS)
    
    while True:
        print(f"\n开始第{current_level}关!")
        game = NailGame(current_level)
        
        while not game.is_level_complete():
            game.display_nails()
            print(f"当前玩家: 玩家{game.current_player}")
            
            try:
                nail_id = int(input(f"请输入要拔出的钉子编号(1-{len(game.nails)}),输入0退出游戏: "))
                
                if nail_id == 0:
                    print("游戏已退出!")
                    return
                    
                if nail_id not in game.nails:
                    print(f"无效的钉子编号,请输入1-{len(game.nails)}之间的数字!")
                    continue
                    
                if game.remove_nail(nail_id):
                    print(f"成功拔出钉子{nail_id}!")
                else:
                    print(f"无法拔出钉子{nail_id},请确保其依赖的钉子已经被拔出!")
                    
            except ValueError:
                print("请输入有效的数字!")
                continue
        
        winner = 3 - game.current_player
        print(f"\n恭喜!玩家{winner}赢得了第{current_level}关!")
        
        if current_level < max_level:
            while True:
                try:
                    next_level = input("\n是否进入下一关? (y/n): ").lower()
                    if next_level in ['y', 'n']:
                        break
                    print("请输入 y 或 n")
                except Exception:
                    print("输入错误，请重试")
            
            if next_level == 'y':
                current_level += 1
                continue
            else:
                print("感谢游玩!")
                break
        else:
            print("\n恭喜你通关了所有关卡!")
            break

if __name__ == "__main__":
    main() 