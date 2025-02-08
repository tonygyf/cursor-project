"""
@description 拔钉子游戏关卡配置
@author Your Name
@date 2024
"""

class NailType:
    """
    钉子类型定义
    """
    RED = 'red'
    BLUE = 'blue'
    GREEN = 'green'
    YELLOW = 'yellow'
    PURPLE = 'purple'

    @staticmethod
    def get_color(nail_type):
        """
        获取钉子类型对应的RGB颜色
        """
        colors = {
            'red': (255, 0, 0),      # 动物类
            'blue': (0, 0, 255),     # 植物类
            'green': (0, 255, 0),    # 物品类
            'yellow': (255, 255, 0),  # 场景类
            'purple': (128, 0, 128)   # 特殊类
        }
        return colors.get(nail_type, (128, 128, 128))

class LevelConfig:
    """
    关卡配置类
    """
    def __init__(self, level_num, description, width, height, stack_size):
        """
        @param level_num: 关卡编号
        @param description: 关卡描述
        @param width: 显示宽度
        @param height: 显示高度
        @param stack_size: 栈大小限制
        """
        self.level_num = level_num
        self.description = description
        self.width = width
        self.height = height
        self.stack_size = stack_size
        self.nail_positions = {}  # 存储钉子位置 {id: (x, y)}
        self.dependencies = {}    # 存储依赖关系 {id: [依赖的钉子id列表]}
        self.nail_types = {}      # {id: nail_type}
        self.nail_descriptions = {}  # 新增：钉子描述

# 定义关卡
LEVEL_1 = LevelConfig(1, "简单三角形", 3, 3, 3)
LEVEL_1.nail_positions = {
    1: (1, 0),
    2: (0, 2),
    3: (2, 2)
}
LEVEL_1.dependencies = {
    2: [1],
    3: [1]
}
LEVEL_1.nail_types = {
    1: NailType.RED,
    2: NailType.RED,
    3: NailType.BLUE
}

LEVEL_2 = LevelConfig(2, "小型生态系统", 5, 5, 4)
LEVEL_2.nail_positions = {
    1: (2, 0),  # 太阳
    2: (1, 2),  # 树
    3: (3, 2),  # 草
    4: (0, 3),  # 兔子
    5: (2, 3),  # 虫子
    6: (4, 3),  # 鸟
    7: (2, 4)   # 土地
}
LEVEL_2.dependencies = {
    2: [1],     # 树依赖太阳
    3: [1],     # 草依赖太阳
    4: [2, 3],  # 兔子依赖树和草
    5: [3],     # 虫子依赖草
    6: [5],     # 鸟依赖虫子
    7: [2, 3]   # 土地依赖树和草
}
LEVEL_2.nail_types = {
    1: NailType.YELLOW,  # 太阳
    2: NailType.BLUE,    # 树
    3: NailType.BLUE,    # 草
    4: NailType.RED,     # 兔子
    5: NailType.RED,     # 虫子
    6: NailType.RED,     # 鸟
    7: NailType.GREEN    # 土地
}
LEVEL_2.nail_descriptions = {
    1: "太阳：为生态系统提供能量",
    2: "树：提供氧气和庇护",
    3: "草：基础植物",
    4: "兔子：草食动物",
    5: "虫子：小型生物",
    6: "鸟：捕食者",
    7: "土地：生态基础"
}

LEVEL_3 = LevelConfig(3, "城市发展", 7, 7, 5)
LEVEL_3.nail_positions = {
    1: (3, 0),   # 规划
    2: (1, 1),   # 道路
    3: (3, 1),   # 电力
    4: (5, 1),   # 水利
    5: (0, 3),   # 住宅
    6: (2, 3),   # 商业
    7: (4, 3),   # 工业
    8: (6, 3),   # 公园
    9: (1, 5),   # 学校
    10: (3, 5),  # 医院
    11: (5, 5),  # 文化中心
    12: (3, 6)   # 环保系统
}
LEVEL_3.dependencies = {
    2: [1],        # 道路依赖规划
    3: [1],        # 电力依赖规划
    4: [1],        # 水利依赖规划
    5: [2, 3, 4],  # 住宅依赖基础设施
    6: [2, 3, 4],  # 商业依赖基础设施
    7: [2, 3, 4],  # 工业依赖基础设施
    8: [2],        # 公园依赖道路
    9: [5, 6],     # 学校依赖住宅和商业
    10: [5, 6],    # 医院依赖住宅和商业
    11: [6],       # 文化中心依赖商业
    12: [7, 8]     # 环保系统依赖工业和公园
}
LEVEL_3.nail_types = {
    1: NailType.PURPLE,  # 规划
    2: NailType.GREEN,   # 道路
    3: NailType.GREEN,   # 电力
    4: NailType.GREEN,   # 水利
    5: NailType.YELLOW,  # 住宅
    6: NailType.YELLOW,  # 商业
    7: NailType.YELLOW,  # 工业
    8: NailType.BLUE,    # 公园
    9: NailType.RED,     # 学校
    10: NailType.RED,    # 医院
    11: NailType.RED,    # 文化中心
    12: NailType.BLUE    # 环保系统
}
LEVEL_3.nail_descriptions = {
    1: "城市规划：发展蓝图",
    2: "道路系统：交通网络",
    3: "电力系统：能源供应",
    4: "水利系统：水资源管理",
    5: "住宅区：居民生活",
    6: "商业区：经济活动",
    7: "工业区：生产制造",
    8: "公园：休闲娱乐",
    9: "学校：教育资源",
    10: "医院：医疗保障",
    11: "文化中心：文化活动",
    12: "环保系统：环境保护"
}

# 第四关：圣诞树 - 超大松散版本
LEVEL_4 = LevelConfig(4, "巨型圣诞树", 40, 45, 6)  # 显著增加游戏区域

def create_christmas_tree():
    positions = {}
    dependencies = {}
    nail_types = {}
    descriptions = {}
    nail_id = 1

    # 树顶星星
    positions[nail_id] = (20, 1)  # 移到新的中心位置
    nail_types[nail_id] = NailType.YELLOW
    descriptions[nail_id] = "树顶星：圣诞树的点缀"
    star_id = nail_id
    nail_id += 1

    # 树的主体结构
    levels = 10  # 减少层数，但每层间距更大
    max_width = 35  # 显著增加最大宽度
    vertical_spacing = 4  # 显著增加垂直间距
    
    # 存储每层的钉子ID
    layer_nails = []
    
    # 创建树的主体结构
    for level in range(levels):
        layer_nails.append([])
        width = min(5 + level * 4, max_width)  # 每层宽度增加更多
        start_x = 20 - width // 2
        y = level * vertical_spacing + 5  # 从更低的位置开始
        
        # 水平间距随层数增加
        horizontal_spacing = 3 if level < 3 else 4 if level < 6 else 5
        
        # 计算这一层的钉子数量
        num_nails = width // horizontal_spacing + 1
        
        for i in range(num_nails):
            x = start_x + i * horizontal_spacing
            if x < start_x + width:
                positions[nail_id] = (x, y)
                
                # 设置依赖关系
                if level == 0:
                    dependencies[nail_id] = [star_id]
                else:
                    deps = []
                    # 依赖上一层的相邻钉子，但范围更大
                    prev_layer = layer_nails[level - 1]
                    for prev_id in prev_layer:
                        prev_x, prev_y = positions[prev_id]
                        if abs(prev_x - x) <= horizontal_spacing * 1.5:  # 增加依赖范围
                            deps.append(prev_id)
                    if deps:
                        dependencies[nail_id] = deps
                    else:
                        continue
                
                # 设置类型和描述 - 增加更多变化
                if i % 4 == 0:
                    nail_types[nail_id] = NailType.RED
                    descriptions[nail_id] = "红色大球装饰"
                elif i % 4 == 1:
                    nail_types[nail_id] = NailType.GREEN
                    descriptions[nail_id] = "松树枝"
                elif i % 4 == 2:
                    nail_types[nail_id] = NailType.BLUE
                    descriptions[nail_id] = "蓝色LED灯"
                else:
                    nail_types[nail_id] = NailType.YELLOW
                    descriptions[nail_id] = "金色小铃铛"
                
                layer_nails[level].append(nail_id)
                nail_id += 1

    # 更大的树干
    trunk_height = 6
    trunk_width = 8
    trunk_start_x = 16
    trunk_start_y = levels * vertical_spacing + 5
    
    # 创建更稀疏的树干
    for y in range(trunk_height):
        for x in range(trunk_width):
            if (x + y) % 3 == 0:  # 更稀疏的模式
                positions[nail_id] = (trunk_start_x + x, trunk_start_y + y)
                dependencies[nail_id] = layer_nails[-1]
                nail_types[nail_id] = NailType.PURPLE
                descriptions[nail_id] = "树干结构"
                nail_id += 1

    # 添加更多分散的装饰品
    decorations = [
        (10, 8, NailType.YELLOW, "大型金色铃铛"),
        (30, 8, NailType.YELLOW, "大型金色铃铛"),
        (8, 16, NailType.RED, "巨型蝴蝶结"),
        (32, 16, NailType.RED, "巨型蝴蝶结"),
        (15, 24, NailType.YELLOW, "金色糖果棒"),
        (25, 24, NailType.YELLOW, "金色糖果棒"),
        (12, 12, NailType.PURPLE, "紫色彩带"),
        (28, 12, NailType.PURPLE, "紫色彩带"),
        (14, 20, NailType.RED, "礼物盒"),
        (26, 20, NailType.RED, "礼物盒"),
        (20, 28, NailType.YELLOW, "大型装饰星"),
        (8, 28, NailType.BLUE, "冰柱装饰"),
        (32, 28, NailType.BLUE, "冰柱装饰"),
        (14, 32, NailType.GREEN, "松果装饰"),
        (26, 32, NailType.GREEN, "松果装饰"),
        (20, 36, NailType.RED, "圣诞老人"),
        (10, 36, NailType.BLUE, "雪人"),
        (30, 36, NailType.BLUE, "驯鹿")
    ]
    
    for x, y, type_, desc in decorations:
        positions[nail_id] = (x, y)
        deps = []
        for other_id, (other_x, other_y) in positions.items():
            if abs(other_x - x) <= 5 and abs(other_y - y) <= 5 and other_id < nail_id:
                deps.append(other_id)
        if deps:
            dependencies[nail_id] = deps
            nail_types[nail_id] = type_
            descriptions[nail_id] = desc
            nail_id += 1

    return positions, dependencies, nail_types, descriptions

# 生成圣诞树数据
tree_positions, tree_dependencies, tree_types, tree_descriptions = create_christmas_tree()

# 将生成的数据添加到关卡配置中
LEVEL_4.nail_positions = tree_positions
LEVEL_4.dependencies = tree_dependencies
LEVEL_4.nail_types = tree_types
LEVEL_4.nail_descriptions = tree_descriptions

# 存储所有关卡
LEVELS = {
    1: LEVEL_1,
    2: LEVEL_2,
    3: LEVEL_3,
    4: LEVEL_4
}

