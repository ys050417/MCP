import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    print("🔌 正在连接 MCP 服务端...")

    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"],
        env=None
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            print("✅ MCP 服务连接成功！")

            tools = await session.list_tools()
            tool_list = tools.tools

            while True:
                print("\n===== MCP 工具菜单 =====")
                print("1. 查看桌面文件列表")
                print("2. 使用计算器")
                print("0. 退出程序")
                choice = input("请选择功能（0/1/2）：")

                # 退出
                if choice == "0":
                    print("👋 正在退出...")
                    break

                # 查看桌面文件
                elif choice == "1":
                    print("\n🖼️ 获取桌面文件列表...")
                    file_result = await session.call_tool(
                        name="get_desktop_files",
                        arguments={}
                    )
                    if len(file_result.content) > 0:
                        print(f"桌面文件：{file_result.content[0].text}")
                    else:
                        print("桌面文件：空或读取失败")

                # 计算器
                elif choice == "2":
                    try:
                        print("\n🧮 计算器模式")
                        a = float(input("请输入第 1 个数字："))
                        b = float(input("请输入第 2 个数字："))
                        op = input("请输入运算符（+ - * /）：")

                        calc_result = await session.call_tool(
                            name="calculator",
                            arguments={
                                "a": a,
                                "b": b,
                                "operator": op
                            }
                        )
                        print(f"✅ 结果：{calc_result.content[0].text}")
                    except Exception as e:
                        print(f"❌ 计算失败：{str(e)}")

                else:
                    print("⚠️ 无效选项，请重新输入！")

    print("\n🎉 已断开连接，程序结束！")

if __name__ == "__main__":
    asyncio.run(main())