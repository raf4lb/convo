export function ConversationLoading() {
  const conversations = [1, 2, 3, 4];
  return (
    <div className="w-96 bg-white border-r border-neutral-200 items-center justify-center text-neutral-500">
      {conversations.map((item) => (
        <div key={item} className="w-full p-4 border-b border-neutral-100 text-left animate-pulse">
          <div className="flex items-start gap-3">
            {/* Avatar */}
            <div className="size-11 rounded-full bg-gray-200"></div>
            <div className="flex-1 min-w-0">
              <div className="flex items-start justify-between mb-1">
                <div className="flex-1 min-w-0">
                  {/* Customer Name */}
                  <p className="bg-gray-200 rounded w-52 h-3.5 mt-1 mb-2"></p>
                  {/* Customer Phone */}
                  <p className="bg-gray-200 rounded w-30 h-2.5 mt-1"></p>
                </div>
                {/* Time */}
                <span className="bg-gray-200 rounded w-8 h-2 mt-1 ml-2"></span>
              </div>
              {/* Last Message */}
              <p className="bg-gray-200 rounded w-48 h-3 mb-1 mt-5.5"></p>
              {/* Assigned To */}
              <p className="bg-gray-200 rounded w-20 h-2.5 mb-1 mt-5 ml-2"></p>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
