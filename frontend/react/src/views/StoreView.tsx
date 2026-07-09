import { useState, useEffect } from 'react';

import { getStores, createStore } from '../api/storeApi';
import type { StoreResponse } from '../types/store';

interface StoreViewProps {
  onStoreSelect: (storeId: number, storeName: string) => void;
}

export default function StoreView({ onStoreSelect }: StoreViewProps) {
  const [stores, setStores] = useState<StoreResponse[]>([]);
  const [selectedStoreId, setSelectedStoreId] = useState<number | null>(null);

  const loadStores = async () => {
    try {
      const data = await getStores();
      setStores(data || []);
    } catch (error) {
      console.error('매장 조회 실패:', error);
    }
  };

  // 화면이 처음 켜질 때 백엔드에서 매장 목록을 자동으로 땡겨옵니다.
  useEffect(() => {
    loadStores();
  }, []);

    const handleAddStore = async () => {
      const storeName = prompt('매장 이름을 입력하세요 :');
      if (!storeName || !storeName.trim()) return;

      // ➕ 백엔드가 location을 필수로 요구하므로, 위치 정보도 같이 팝업으로 받습니다!
      const storeLocation = prompt('매장의 위치를 입력하세요 :');
      if (!storeLocation || !storeLocation.trim()) return;

      try {
        // 🚀 백엔드 스키마와 완벽하게 싱크를 맞춰 name과 location을 둘 다 보냅니다!
        await createStore({ 
          name: storeName.trim(), 
          location: storeLocation.trim() 
        });
        loadStores(); // 등록 성공하면 목록 새로고침
      } catch (error) {
        alert('매장 등록 실패: 백엔드 서버나 DB 연결을 확인하세요.');
      }
    };

  return (
    <div style={{ padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
      <h2>🏢 매장</h2>

      {/* 매장 목록 리스트 (PySide6의 QListWidget과 동일) */}
      <div style={{ border: '1px solid #ccc', minHeight: '150px', marginBottom: '15px', borderRadius: '4px', backgroundColor: '#fff' }}>
        {stores.length === 0 ? (
          <p style={{ padding: '10px', color: '#888' }}>등록된 매장이 없습니다. [매장 생성]을 눌러주세요.</p>
        ) : (
          stores.map((store) => (
            <div
              key={store.id}
              onClick={() => setSelectedStoreId(store.id)}
              onDoubleClick={() => onStoreSelect(store.id, store.name)} // 더블클릭 신호 전송
              style={{
                padding: '10px',
                cursor: 'pointer',
                backgroundColor: selectedStoreId === store.id ? '#e0f7fa' : 'transparent',
                borderBottom: '1px solid #eee',
                fontWeight: selectedStoreId === store.id ? 'bold' : 'normal'
              }}
            >
              {store.name} ({store.location})
            </div>
          ))
        )}
      </div>

      {/* 하단 제어 버튼 */}
      <div style={{ display: 'flex', gap: '10px' }}>
        <button onClick={loadStores} style={{ padding: '10px 20px', cursor: 'pointer' }}>매장 조회</button>
        <button onClick={handleAddStore} style={{ padding: '10px 20px', cursor: 'pointer', backgroundColor: '#e6f7ff', border: '1px solid #91d5ff' }}>매장 생성</button>
      </div>
    </div>
  );
}