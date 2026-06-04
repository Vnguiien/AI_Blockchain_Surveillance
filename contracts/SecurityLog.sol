// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SecurityLog {
    struct Evidence {
        uint256 id;
        string behaviorType;
        string videoHash;
        string evidenceImage;
        string timestampText;
        address reporter;
        uint256 blockTime;
    }

    uint256 public totalEvidence;

    mapping(uint256 => Evidence) public evidences;

    event EvidenceAdded(
        uint256 indexed id,
        string behaviorType,
        string videoHash,
        string evidenceImage,
        string timestampText,
        address indexed reporter,
        uint256 blockTime
    );

    function addEvidence(
        string memory _behaviorType,
        string memory _videoHash,
        string memory _evidenceImage,
        string memory _timestampText
    ) public {
        totalEvidence++;

        evidences[totalEvidence] = Evidence(
            totalEvidence,
            _behaviorType,
            _videoHash,
            _evidenceImage,
            _timestampText,
            msg.sender,
            block.timestamp
        );

        emit EvidenceAdded(
            totalEvidence,
            _behaviorType,
            _videoHash,
            _evidenceImage,
            _timestampText,
            msg.sender,
            block.timestamp
        );
    }

    function getEvidence(uint256 _id) public view returns (
        uint256,
        string memory,
        string memory,
        string memory,
        string memory,
        address,
        uint256
    ) {
        Evidence memory e = evidences[_id];

        return (
            e.id,
            e.behaviorType,
            e.videoHash,
            e.evidenceImage,
            e.timestampText,
            e.reporter,
            e.blockTime
        );
    }
}