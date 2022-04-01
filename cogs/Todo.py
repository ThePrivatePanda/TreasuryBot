from nextcord.ext import commands


class Todo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(name="todo")
    async def todo(self, ctx):
        pass

    @todo.command(name="add")
    async def todo_add(self, ctx, *, task):

        todos = self.bot.todo.get(str(ctx.author.id))
        print(todos)
        print(type(todos))
        if todos:
            todos = todos.append(task)
            self.bot.todo.update(str(ctx.author.id), todos)
        else:
            self.bot.todo.update(str(ctx.author.id), [task])

        return await ctx.send("Done.")

    @todo.command(name="list")
    async def todo_list(self, ctx):
        todos = self.bot.todo.get(str(ctx.author.id))
        if not todos:
            return await ctx.reply("You have no todos!")
        else:
            return await ctx.reply("\n".join(todos))

def setup(bot):
    bot.add_cog(Todo(bot))