import React, { useState } from 'react';
import UnifiedMap from './UnifiedMap';
import AtAGlance from './AtAGlance';
import PolicyGovernance from './PolicyGovernance';
import StrategicPlanning from './StrategicPlanning';
import ResearchHub from './ResearchHub';
import AdvancedHydrology from './AdvancedHydrology';
import PublicInfo from './PublicInfo';
import FullReport from './FullReport';

const tabs = [
  "🗺️ Unified Map View",
  "📊 At-a-Glance Dashboard",
  "⚖️ Policy & Governance",
  "🏛️ Strategic Planning",
  "🔬 Research Hub",
  "💧 Public Info",
  "🔬 Advanced Hydrology",
  "📋 Generate Full Report"
];

export default function DashboardTabs(props) {
  const [selectedTab, setSelectedTab] = useState(tabs[0]);
  return (
    <>
      <nav>
        {tabs.map(tab => (
          <button key={tab} onClick={() => setSelectedTab(tab)}>{tab}</button>
        ))}
      </nav>
      <section>
        {selectedTab === tabs[0] && <UnifiedMap {...props} />}
        {selectedTab === tabs[1] && <AtAGlance {...props} />}
        {selectedTab === tabs[2] && <PolicyGovernance {...props} />}
        {selectedTab === tabs[3] && <StrategicPlanning {...props} />}
        {selectedTab === tabs[4] && <ResearchHub {...props} />}
        {selectedTab === tabs[5] && <PublicInfo {...props} />}
        {selectedTab === tabs[6] && <AdvancedHydrology {...props} />}
        {selectedTab === tabs[7] && <FullReport {...props} />}
      </section>
    </>
  );
}
