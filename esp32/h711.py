from machine import Pin
import utime


class Hx711:
    def __init__(self, clk_pin: int, data_pin: int):
        """
        HX711 模块初始化
        :param clk_pin: 时钟引脚号
        :param data_pin: 数据引脚号
        """
        self.clk = Pin(clk_pin, Pin.OUT)
        self.data = Pin(data_pin, Pin.IN)
        self.clk.value(0)
        self.last_value = self.getValue()

    def getValue(self) -> int:
        """
        从 HX711 获取 24 位数据
        :return: 数据值（补码格式）
        """
        while self.data.value() == 1:
            utime.sleep_ms(1)

        count = 0
        for _ in range(24):
            self.clk.value(1)
            count = (count << 1) | self.data.value()
            self.clk.value(0)

        self.clk.value(1)
        count ^= 0x800000  # 补码转换
        self.clk.value(0)
        return count


class EleScale(Hx711):
    def __init__(self, clk_pin: int, data_pin: int, cap_value: float):
        """
        电子秤初始化
        :param clk_pin: 时钟引脚号
        :param data_pin: 数据引脚号
        :param cap_value: 转换因子（单位值对应的传感器输出）
        """
        super().__init__(clk_pin, data_pin)
        self.no_load_offset = self.__hx711_read()  # 初始零点偏移值
        self.cap_value = cap_value

    def __hx711_read(self, times: int = 5, a: float = 0.8) -> int:
        """
        获取 HX711 的平滑值
        :param times: 采样次数
        :param a: 平滑系数（指数平滑滤波）
        :return: 平滑后的读数值
        """
        if times < 3:
            times = 3

        values = []
        for _ in range(times):
            raw = self.getValue()
            smooth = raw * a + self.last_value * (1 - a)  # 平滑处理
            self.last_value = smooth  # 更新历史值
            values.append(smooth)

        values.sort()
        # print(int(sum(values[1:-1]) // (times - 2)))
        return int(values[times // 2])

    def tare(self):
        """
        零点校准，在空载状态下调用。
        """
        self.no_load_offset = self.__hx711_read(times=11)
        print(f"零点初始值: {self.no_load_offset}")

    def getWeight(self) -> float:
        """
        获取当前重量值
        :return: 当前重量，单位：g
        """
        raw_data = self.__hx711_read(5) - self.no_load_offset
        print(raw_data)
        weight = raw_data / self.cap_value
        return max(0.0, weight)

