import { ModeToggle } from "@/components/mode-toggle";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Bot, Code2, FileText, Send, Terminal, User } from "lucide-react";

export default function Home() {
  return (
    <div className="flex h-screen w-full flex-col bg-background md:flex-row">
      {/* Sidebar */}
      <aside className="w-full border-r bg-muted/40 md:w-[300px] md:flex-col lg:w-[350px]">
        <div className="flex h-14 items-center border-b px-4 lg:h-[60px]">
          <div className="flex items-center gap-2 font-semibold">
            <Bot className="h-6 w-6" />
            <span>LISA Agentic</span>
          </div>
          <div className="ml-auto">
            <ModeToggle />
          </div>
        </div>
        <div className="flex-1 overflow-auto py-4">
          <ScrollArea className="h-full px-4">
            <div className="space-y-4">
              <div>
                <h3 className="mb-2 px-2 text-sm font-semibold tracking-tight">Active Session</h3>
                <div className="space-y-1">
                  <Button variant="secondary" className="w-full justify-start">
                    <FileText className="mr-2 h-4 w-4" />
                    New Project Setup
                  </Button>
                </div>
              </div>

              <Separator />

              <div>
                <h3 className="mb-2 px-2 text-sm font-semibold tracking-tight">History</h3>
                <div className="space-y-1">
                  <Button variant="ghost" className="w-full justify-start text-muted-foreground">
                    Authentication Flow
                  </Button>
                  <Button variant="ghost" className="w-full justify-start text-muted-foreground">
                    Database Schema
                  </Button>
                </div>
              </div>
            </div>
          </ScrollArea>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex flex-1 flex-col overflow-hidden">
        {/* Header/Status Bar */}
        <header className="flex h-14 items-center gap-4 border-b bg-muted/40 px-6 lg:h-[60px]">
          <span className="font-semibold">Current Task: Initial Setup</span>
          <div className="ml-auto flex items-center gap-2">
            <span className="text-xs text-muted-foreground">Agents: Idle</span>
          </div>
        </header>

        {/* Content Area */}
        <div className="flex flex-1 overflow-hidden">
          {/* Chat/Interaction Panel */}
          <div className="flex w-1/2 flex-col border-r">
            <ScrollArea className="flex-1 p-4">
              <div className="space-y-4">
                {/* Example Messages */}
                <div className="flex gap-3">
                  <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary/10">
                    <User className="h-4 w-4" />
                  </div>
                  <div className="bg-muted p-3 rounded-lg text-sm max-w-[80%]">
                    Can you verify the `state.py` file?
                  </div>
                </div>

                <div className="flex gap-3">
                  <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary text-primary-foreground">
                    <Bot className="h-4 w-4" />
                  </div>
                  <div className="bg-primary/10 p-3 rounded-lg text-sm max-w-[80%]">
                    I've checked `state.py` and noticed a missing import. I'll fix that.
                  </div>
                </div>
              </div>
            </ScrollArea>
            <div className="p-4 border-t">
              <div className="relative">
                <Input placeholder="Describe your task..." className="pr-12" />
                <Button size="icon" className="absolute right-1 top-1 h-8 w-8" variant="ghost">
                  <Send className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </div>

          {/* Workspace/Artifacts Panel */}
          <div className="flex flex-1 flex-col bg-muted/10">
            <Tabs defaultValue="code" className="flex-1 flex flex-col">
              <div className="flex items-center justify-between px-4 py-2 border-b">
                <TabsList>
                  <TabsTrigger value="code" className="flex items-center gap-2">
                    <Code2 className="h-4 w-4" /> Code
                  </TabsTrigger>
                  <TabsTrigger value="terminal" className="flex items-center gap-2">
                    <Terminal className="h-4 w-4" /> Terminal
                  </TabsTrigger>
                </TabsList>
              </div>

              <div className="flex-1 overflow-hidden p-4">
                <TabsContent value="code" className="h-full m-0">
                  <Card className="h-full flex flex-col border-0 shadow-none">
                    <CardHeader className="p-4 border-b">
                      <CardTitle className="text-sm font-mono">state/state.py</CardTitle>
                    </CardHeader>
                    <CardContent className="flex-1 p-0 overflow-hidden font-mono text-sm">
                      <ScrollArea className="h-full p-4">
                        <pre className="text-muted-foreground">
                          {`from typing import TypedDict, List
                                            
class AgentState(TypedDict):
    user_request: str
    plan: dict # Architect's plan
    code: str # Coder's output
    review_feedback: str`}
                        </pre>
                      </ScrollArea>
                    </CardContent>
                  </Card>
                </TabsContent>

                <TabsContent value="terminal" className="h-full m-0">
                  <Card className="h-full flex flex-col border-0 shadow-none bg-black text-white">
                    <CardContent className="flex-1 p-4 font-mono text-xs">
                      <div className="text-green-400">$ python app.py</div>
                      <div>Starting agents...</div>
                      <div>Architect agent initialized.</div>
                    </CardContent>
                  </Card>
                </TabsContent>
              </div>
            </Tabs>
          </div>
        </div>
      </main>
    </div>
  );
}
