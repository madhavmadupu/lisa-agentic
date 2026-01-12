"use client";

import { ScrollArea } from "@/components/ui/scroll-area";
import { cn } from "@/lib/utils";
import { File } from "lucide-react";

interface FileTreeProps {
    files: string[];
    onSelect: (path: string) => void;
    className?: string;
}

export function FileTree({ files, onSelect, className }: FileTreeProps) {
    return (
        <div className={cn("text-sm", className)}>
            <ScrollArea className="h-full">
                <div className="flex flex-col gap-1 p-2">
                    {files.length === 0 && (
                        <div className="text-muted-foreground p-2 text-xs">No files in workspace</div>
                    )}
                    {files.map((file) => (
                        <button
                            key={file}
                            onClick={() => onSelect(file)}
                            className="flex items-center gap-2 px-2 py-1.5 hover:bg-muted/50 rounded-sm text-left w-full truncate"
                        >
                            <File className="h-4 w-4 shrink-0 text-muted-foreground" />
                            <span className="truncate">{file}</span>
                        </button>
                    ))}
                </div>
            </ScrollArea>
        </div>
    );
}
